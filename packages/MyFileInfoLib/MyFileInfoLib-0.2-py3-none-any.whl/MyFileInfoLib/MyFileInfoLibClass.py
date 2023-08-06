import os

class MyfileInfoLibClass:
    """
    This class finds the oldest and earliest created, the biggest and the smallest file from your entered files.
    It has got some methods:
    GetTheOldestFileName   - it chooses the oldest file
    GetTheNewestFileName - it chooses the earliest file
    GetTheBiggestFileName  - it chooses the biggest file
    GetTheSmallestFileName - it chooses the smallest file
    """

    def __init__ ( self, *files: str ):
        self.files = files

    def GetTheOldestFileName ( self ):
        values = {  }
        for file in self.files:
            name = file
            info = os.stat ( file )
            timef = info.st_ctime
            values [name] = timef
        sortedKeys = sorted ( values, key = values.get, reverse = False )
        return sortedKeys [ 0 ]

    def GetTheNewestFileName ( self ):
        values = {  }
        for file in self.files:
            name = file
            info = os.stat ( file )
            timef = info.st_ctime
            values [name] = timef
        sortedKeys = sorted ( values, key = values.get, reverse = True )
        return sortedKeys [ 0 ]        

    def GetTheBiggestFileName ( self ):
        values = {  }
        for file in self.files:
            name = file
            info = os.stat ( file )
            fileSize = info.st_size
            values [name] = fileSize
        sortedKeys = sorted ( values, key = values.get, reverse = True )
        return sortedKeys [ 0 ]

    def GetTheSmallestFileName ( self ):
        values = {  }
        for file in self.files:
            name = file
            info = os.stat ( file )
            fileSize = info.st_size
            values [name] = fileSize
        sortedKeys = sorted ( values, key = values.get, reverse = False )
        return sortedKeys [ 0 ]   

    def GetAllInformation ( self ):
        newfile = str
        oldFile = self.GetTheOldestFileName (  )
        newFile = self.GetTheNewFileName (  )
        bigFile = self.GetTheBiggestFileName (  )
        smallFile = self.GetTheSmallestFileName (  )
        result = " New file:\t " + str ( oldFile ) + "\n Old file:\t " + str ( newFile ) + "\n Big file:\t " + str ( bigFile ) + "\n Small file:\t "+  str ( smallFile )
        return result