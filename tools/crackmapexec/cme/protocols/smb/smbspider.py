from time import strftime, localtime
from cme.protocols.smb.remotefile import RemoteFile
from impacket.smb3structs import FILE_READ_DATA
from impacket.smbconnection import SessionError
import logging
import re
import traceback

class SMBSpider:

    def __init__(self, smbconnection, logger):
        self.smbconnection = smbconnection
        self.logger = logger
        self.share = None
        self.regex = []
        self.pattern = []
        self.folder = None
        self.exclude_dirs = []
        self.onlyfiles = True
        self.content = False
        self.results = []

    def spider(self, share, folder='.', pattern=[], regex=[], exclude_dirs=[], depth=None, content=False, onlyfiles=True):
        if regex:
            try:
                self.regex = [re.compile(rx) for rx in regex]
            except Exception as e:
                self.logger.error('Regex compilation error: {}'.format(e))

        self.folder = folder
        self.pattern = pattern
        self.exclude_dirs = exclude_dirs
        self.content = content
        self.onlyfiles = onlyfiles

        if share == "*":
            self.logger.info("Enumerating shares for spidering")
            permissions = []
            try:
                for share in self.smbconnection.listShares():
                    share_name = share['shi1_netname'][:-1]
                    share_remark = share['shi1_remark'][:-1]
                    try:
                        self.smbconnection.listPath(share_name, '*')
                        self.share = share_name
                        self.logger.info("Spidering share: {0}".format(share_name))
                        self._spider(folder, depth)
                    except SessionError:
                        pass
            except Exception as e:
                self.logger.error('Error enumerating shares: {}'.format(e))
        else:
            self.share = share
            self.logger.info("Spidering {0}".format(folder))
            self._spider(folder, depth)

        return self.results

    def _spider(self, subfolder, depth):
        '''
            Abondon all hope ye who enter here.
            You're now probably wondering if I was drunk and/or high when writing this.
            Getting this to work took a toll on my sanity. So yes. a lot.
        '''

        # The following is some funky shit that deals with the way impacket treats file paths

        if subfolder in ['', '.']:
            subfolder = '*'

        elif subfolder.startswith('*/'):
            subfolder = subfolder[2:] + '/*'
        else:
            subfolder = subfolder.replace('/*/', '/') + '/*'

        # End of the funky shit... or is it? Surprise! This whole thing is funky

        filelist = None
        try:
            filelist = self.smbconnection.listPath(self.share, subfolder)
            self.dir_list(filelist, subfolder)
            if depth == 0:
                return
        except SessionError as e:
            if not filelist:
                if 'STATUS_ACCESS_DENIED' not in str(e):
                    logging.debug("Failed listing files on share {} in directory {}: {}".format(self.share, subfolder, e))
                return

        for result in filelist:
            if result.is_directory() and result.get_longname() not in ['.','..']:
                if subfolder == '*':
                    self._spider(subfolder.replace('*', '') + result.get_longname(), depth-1 if depth else None)
                elif subfolder != '*' and (subfolder[:-2].split('/')[-1] not in self.exclude_dirs):
                    self._spider(subfolder.replace('*', '') + result.get_longname(), depth-1 if depth else None)
        return

    def dir_list(self, files, path):
        path = path.replace('*', '')
        for result in files:
            for pattern in self.pattern:
                if result.get_longname().lower().find(pattern.lower()) != -1:
                    if not self.onlyfiles and result.is_directory():
                        self.logger.highlight(u"//{}/{}/{}{} [dir]".format(self.smbconnection.getRemoteHost(), self.share, 
                                                                           path, 
                                                                           result.get_longname()))
                    else:
                        self.logger.highlight(u"//{}/{}/{}{} [lastm:'{}' size:{}]".format(self.smbconnection.getRemoteHost(), self.share,
                                                                                       path,
                                                                                       result.get_longname(),
                                                                                       'n\\a' if not self.get_lastm_time(result) else self.get_lastm_time(result),
                                                                                       result.get_filesize()))
                    self.results.append('{}{}'.format(path, result.get_longname()))

            for regex in self.regex:
                if regex.findall(result.get_longname()):
                    if not self.onlyfiles and result.is_directory():
                        self.logger.highlight(u"//{}/{}/{}{} [dir]".format(self.smbconnection.getRemoteHost(), self.share, path, result.get_longname()))
                    else:
                        self.logger.highlight(u"//{}/{}/{}{} [lastm:'{}' size:{}]".format(self.smbconnection.getRemoteHost(), self.share,
                                                                                       path,
                                                                                       result.get_longname(),
                                                                                       'n\\a' if not self.get_lastm_time(result) else self.get_lastm_time(result),
                                                                                       result.get_filesize()))

                    self.results.append('{}{}'.format(path, result.get_longname()))

            if self.content:
                if not result.is_directory():
                    self.search_content(path, result)

        return

    def search_content(self, path, result):
        path = path.replace('*', '')
        try:
            rfile = RemoteFile(self.smbconnection, path + result.get_longname(), self.share, access=FILE_READ_DATA)
            rfile.open()

            while True:
                try:
                    contents = rfile.read(4096)
                    if not contents:
                        break
                except SessionError as e:
                    if 'STATUS_END_OF_FILE' in str(e):
                        break

                except Exception:
                    traceback.print_exc()
                    break

                for pattern in self.pattern:
                    if contents.lower().find(pattern.lower()) != -1:
                        self.logger.highlight(u"//{}/{}/{}{} [lastm:'{}' size:{} offset:{} pattern:'{}']".format(self.smbconnection.getRemoteHost(), 
                                                                                                            self.share,
                                                                                                            path,
                                                                                                            result.get_longname(),
                                                                                                            'n\\a' if not self.get_lastm_time(result) else self.get_lastm_time(result),
                                                                                                            result.get_filesize(),
                                                                                                            rfile.tell(),
                                                                                                            pattern))
                        self.results.append('{}{}'.format(path, result.get_longname()))

                for regex in self.regex:
                    if regex.findall(contents):
                        self.logger.highlight(u"//{}/{}/{}{} [lastm:'{}' size:{} offset:{} regex:'{}']".format(self.smbconnection.getRemoteHost(),
                                                                                                          self.share,
                                                                                                          path,
                                                                                                          result.get_longname(),
                                                                                                          'n\\a' if not self.get_lastm_time(result) else self.get_lastm_time(result),
                                                                                                          result.get_filesize(),
                                                                                                          rfile.tell(),
                                                                                                          regex.pattern))
                        self.results.append('{}{}'.format(path, result.get_longname()))

            rfile.close()
            return

        except SessionError as e:
            if 'STATUS_SHARING_VIOLATION' in str(e):
                pass

        except Exception:
            traceback.print_exc()

    def get_lastm_time(self, result_obj):
        lastm_time = None
        try:
            lastm_time = strftime('%Y-%m-%d %H:%M', localtime(result_obj.get_mtime_epoch()))
        except Exception:
            pass

        return lastm_time
