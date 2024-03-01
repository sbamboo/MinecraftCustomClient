# FancyPants/BeautifulPants 1.0 by Simon Kalmi Claesson
# Simple python library to download files or fetch get requests, with the possibility of a progress bar.


from bs4 import BeautifulSoup
import requests,os

from rich.progress import Progress,BarColumn,TextColumn,TimeRemainingColumn,DownloadColumn,TransferSpeedColumn,SpinnerColumn,TaskProgressColumn,RenderableColumn

def get_withProgess_rich(*args, richTitle="[cyan]Downloading...", postDownTxt=None, raise_for_status=False, **kwargs):
    """
    Wrapper function for requests.get that includes a visual loading bar made with rich.
    """
    response = requests.get(*args, **kwargs, stream=True)
    if raise_for_status == True: response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB

    # Initialize the Rich progress bar
    from rich.progress import Progress,BarColumn,TextColumn,TimeRemainingColumn,DownloadColumn,TransferSpeedColumn,SpinnerColumn,TaskProgressColumn,RenderableColumn
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        DownloadColumn(),
        RenderableColumn("[cyan]ETA:"),
        TimeRemainingColumn(compact=True),
        TransferSpeedColumn(),
    ) as progress:
        task = progress.add_task(richTitle, total=total_size, expand=True)

        try:
            # Buffer to store downloaded content
            content_buffer = b''
            for data in response.iter_content(block_size):
                progress.update(task, advance=len(data))
                content_buffer += data

            # Return the response object with downloaded content
            response._content = content_buffer
            if postDownTxt not in ["",None]: print(postDownTxt)
            return response
        except Exception as e:
            # Ensure closing the progress bar and response in case of an exception
            raise e
        finally:
            # Close the progress bar and response
            progress.stop()
            response.close()

def get_withInfo(*args, prefTxt="", suffTxt="", raise_for_status=False, **kwargs):
    """
    Wrapper function for requests.get that takes strings to print before and after downloading.
    """
    if prefTxt not in ["",None]: print(prefTxt)
    response = requests.get(*args, **kwargs)
    if raise_for_status == True: response.raise_for_status()
    if suffTxt not in ["",None]: print(suffTxt)
    return response

def getFile_withProgess_rich(*args, filepath=str, richTitle="[cyan]Downloading...", postDownTxt=None, raise_for_status=True, onFileExiError="raise", **kwargs):
    """
    Wrapper function for requests.get that includes a visual loading bar made with rich while downloading a file.
    To just wrap requests.get without a file use get_withProgess_rich().
    onFileExiError: "raise"/"ignore"/"ignore-with-warn"/"remove"/"remove-with-warn"
    """
    if os.path.exists(filepath):
        onFileExiError = onFileExiError.lower()
        if onFileExiError == "raise":
            raise FileExistsError(f"Failed to download the file: '{filepath}'! File already exists.")
        elif onFileExiError == "remove" or "-with-warn" in onFileExiError:
            if "-with-warn" in onFileExiError:
                print(f"File '{filepath}' already exists, ignoring.")
            if "remove" in onFileExiError: os.remove(filepath)
    response = requests.get(*args, **kwargs, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB

    # Initialize the Rich progress bar
    if response.status_code == 200:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            DownloadColumn(),
            RenderableColumn("[cyan]ETA:"),
            TimeRemainingColumn(compact=True),
            TransferSpeedColumn(),
        ) as progress:
            task = progress.add_task(richTitle, total=total_size, expand=True)
            try:
                # Download to file
                with open(filepath, 'wb') as f:
                    for data in response.iter_content(block_size):
                        progress.update(task, advance=len(data))
                        f.write(data)
                # Return the response object
                if postDownTxt not in ["",None]: print(postDownTxt)
                return response
            except Exception as e:
                # Ensure closing the progress bar and response in case of an exception
                raise e
            finally:
                # Close the progress bar and response
                progress.stop()
                response.close()
    else:
        if raise_for_status == True:
            raise Exception(f"Failed to download the file: '{filepath}'! Invalid status code ({response.status_code}) or empty content.")
        else:
            return response

def getFile_withInfo(*args, filepath=str, prefTxt="", suffTxt="", raise_for_status=True, onFileExiError="raise", **kwargs):
    """
    Wrapper function for requests.get that takes strings to print before and after downloading a file.
    To just wrap requests.get without a file use get_withInfo().
    onFileExiError: "raise"/"ignore"/"ignore-with-warn"/"remove"/"remove-with-warn"
    """
    if prefTxt not in ["",None]: print(prefTxt)
    response = requests.get(*args, **kwargs)
    if response.status_code == 200 and response.content not in ["",None]:
        if not os.path.exists(filepath):
            with open(filepath, 'wb') as file:
                file.write(response.content)
            if suffTxt not in ["",None]: print(suffTxt)
        else:
            onFileExiError = onFileExiError.lower()
            if onFileExiError == "raise":
                raise FileExistsError(f"Failed to download the file: '{filepath}'! File already exists.")
            elif onFileExiError == "remove" or "-with-warn" in onFileExiError:
                if "-with-warn" in onFileExiError:
                    print(f"File '{filepath}' already exists, ignoring.")
                if "remove" in onFileExiError: os.remove(filepath)
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                if suffTxt not in ["",None]: print(suffTxt)
    else:
        if raise_for_status == True:
            raise Exception(f"Failed to download the file: '{filepath}'! Invalid status code ({response.status_code}) or empty content.")
    return response

def getUrlContent_HandleGdriveVirWarn(url,handleGdriveVirWarn=True, loadingBar=False, title="Downloading...", postDownText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there...", raise_for_status=False, yieldResp=False):
    '''Function to send a get request to a url, and if a gdrive-virus-scan-warning apprears try to extract the link and send a get request to it instead.'''
    if loadingBar == True: response = get_withProgess_rich(url,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status)
    else:                  response = get_withInfo(url,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status)
    #response = getter(url)
    if response.status_code == 200:
        # Content of the file
        if "<!DOCTYPE html>" in response.text and "Google Drive - Virus scan warning" in response.text and handleGdriveVirWarn == True:
            print(handleGdriveVirWarnText)
            # attempt extract
            soup = BeautifulSoup(response.text, 'html.parser')
            form = soup.find('form')
            linkBuild = form['action']
            hasParams = False
            inputs = form.find_all('input')
            toBeFound = ["id","export","confirm","uuid"]
            for inp in inputs:
                name = inp.attrs.get('name')
                value = inp.attrs.get('value')
                if name != None and name in toBeFound and value != None:
                    if hasParams == False:
                        pref = "?"
                        hasParams = True
                    else:
                        pref = "&"
                    linkBuild += f"{pref}{name}={value}"
            # Download from built link
            if loadingBar == True: response2 = get_withProgess_rich(linkBuild,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status)
            else:                  response2 = get_withInfo(linkBuild,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status)
            if response2.status_code == 200:
                if yieldResp == True:
                    return response2
                else:
                    return response2.content
            else:
                if yieldResp == True:
                    return response2
                else:
                    return None
        else:
            if yieldResp == True:
                return response
            else:
                return response.content
    # non 200 code
    else:
        if yieldResp == True:
            return response
        else:
            return None

def downloadFile_HandleGdriveVirWarn(url,filepath=str,handleGdriveVirWarn=True, loadingBar=False, title="Downloading...", postDownText="", handleGdriveVirWarnText="Found gdrive scan warning, attempting to extract link and download from there...", raise_for_status=True, encoding="utf-8", onFileExiError="raise", yieldResp=False):
    """Function to try and download a file, and if a gdrive-virus-scan-warning apprears try to extract the link and download it from there.
    onFileExiError: "raise"/"ignore"/"ignore-with-warn"/"remove"/"remove-with-warn"
    """
    if loadingBar == True: response = getFile_withProgess_rich(url,filepath=filepath,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError)
    else:                  response = getFile_withInfo(url,filepath=filepath,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError)
    # Get content of the file
    text_content = None
    if os.path.exists(filepath):
        text_content = open(filepath, 'r', encoding=encoding, errors='replace').read()
        if text_content != None and "<!DOCTYPE html>" in text_content and "Google Drive - Virus scan warning" in text_content and handleGdriveVirWarn == True:
            os.remove(filepath) # clean up
            print(handleGdriveVirWarnText)
            # attempt extract
            soup = BeautifulSoup(text_content, 'html.parser')
            form = soup.find('form')
            linkBuild = form['action']
            hasParams = False
            inputs = form.find_all('input')
            toBeFound = ["id","export","confirm","uuid"]
            for inp in inputs:
                name = inp.attrs.get('name')
                value = inp.attrs.get('value')
                if name != None and name in toBeFound and value != None:
                    if hasParams == False:
                        pref = "?"
                        hasParams = True
                    else:
                        pref = "&"
                    linkBuild += f"{pref}{name}={value}"
            # Download from built link
            if loadingBar == True: response2 = getFile_withProgess_rich(linkBuild,filepath=filepath,richTitle=title,postDownTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError)
            else:                  response2 = getFile_withInfo(linkBuild,filepath=filepath,prefTxt=title,suffTxt=postDownText,raise_for_status=raise_for_status,onFileExiError=onFileExiError)
            if not os.path.exists(filepath):
                raise Exception(f"Download of '{filepath}' seems to have failed! File does not exist.")
            else:
                if yieldResp == True:
                    return response2
        elif yieldResp == True:
            return response
    else:
        if yieldResp == True:
            return response
        else:
            raise Exception(f"Download of '{filepath}' seems to have failed! File does not exist.")
