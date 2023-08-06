import json
import re
from sys import stderr
import os

"""
A class that indicates that some sort of marking is missing. Normally this is any combination of the destination, location and end
"""


class MissingMarkingsException(Exception):
    def __init__(self, missingMarkings, identifier: str):
        super()
        self.__missingMarkings = missingMarkings[:]
        self.__id = identifier

    def __str__(self):
        return "The following markers were not found: " + ", ".join(self.__missingMarkings)

    def getMissinMarkings(self):
        return self.__missingMarkings

    def getIdentifier(self):
        return self.__id


"""
A class that indicates that an identifier is missing. This means that in the JSON object some type of identifier
did not yet exist but we can't create it
"""


class MissingIdentifierException(Exception):
    def __init__(self, identifier: str):
        super()
        self.__id = identifier

    def __str__(self):
        return "The following identifier were not found: " + self.__id

    def getIdentifier(self):
        return self.__id


"""
A class to store code that needs to be written to the JSON
This class is not really needed anymore since it turns out that the json library
already handle '\n' in a string when writing to json, but it might again be needed in the future
if we have to handle that ourselves
"""


class JSONizableCode:
    @staticmethod
    def loadFromJSON(JSONString: str):
        # The replace operation should not be necessary unless we read literally from the json
        # but the json library normally handles this conversion for us
        return JSONizableCode(JSONString.replace('\\n', '\n'))

    def __init__(self, codeStr: str):
        self.__codeString = codeStr

    def getJSONizedCode(self):
        return self.__codeString

    def getCode(self):
        return self.__codeString

# start JSON section


"""
Loads valid JSON from a file
@throws JSONDecodeError if the file did not contain valid JSON
@param fileName: the name of the file to load the JSON from
@returns a JSON object it the file was parsed successfully
"""


def loadJSONFromFile(fileName: str):
    currFile = open(fileName, 'r')
    toReturn = json.load(currFile)
    currFile.close()
    return toReturn


"""
Writes a json object back to a file
@param fileName: the name of the file to write the JSON to
"""


def writeJSONToFile(jsonObj, fileName: str):
    currFile = open(fileName, 'w')
    json.dump(jsonObj, currFile, indent=4)
    currFile.close()


"""
Gets the value that is behind an identifier in a json object given the string that identifies it
@throws MissingIdentifierException if the given identifier is not present in the json object
@param jsonObj: the json object that contains the value
@param identifier: a string that indicates where the value is located
"""


def getFromJSONIdentifier(jsonObj, identifier: str):
    arrayIndexRegex = re.compile("\\[(\\d+)\\]")
    jsonParts = identifier.split(".")
    currLoc = jsonObj
    # recursively walk through the JSON, making the objects and arrays if not yet present
    for i in range(0, len(jsonParts)):
        part = jsonParts[i]
        potMatch = arrayIndexRegex.match(part)
        if potMatch is None:
            if part not in currLoc:
                raise MissingIdentifierException(identifier)
            if (i == len(jsonParts) - 1):
                return currLoc.get(part)
            else:
                currLoc = currLoc.get(part)
        else:
            index = int(potMatch.group(1))
            if part[:potMatch.start()] not in currLoc:
                raise MissingIdentifierException(identifier)
            currLoc = currLoc.get(part[:potMatch.start()])
            if len(currLoc) <= index:
                raise MissingIdentifierException(identifier)
            if (i == len(jsonParts) - 1):
                return currLoc[index]
            else:
                currLoc = currLoc[index]


"""
Write the given string to the json object at the given identifier. Can create this identifier if it is not yet present
@throws MissingIdentifierException if the given identifier is not present in the json object and was not allowed to create it.
@param jsonObj: the json object to write the value to
@param identifier: a string that indicates where the value should be located
@param toWrite: the string to write to the json object
@param makeIdentifier: a Boolean that if set to true will create the identifier in the JSON object if it is not yet present (default is true)
"""


def writeToJSONIdentifier(jsonObj, identifier: str, toWrite: str, makeIdentifier: bool = True):
    arrayIndexRegex = re.compile("\\[(\\d+)\\]")
    jsonParts = identifier.split(".")
    currLoc = jsonObj
    # recursively walk through the JSON, making the objects and arrays if not yet present
    for i in range(0, len(jsonParts)):
        part = jsonParts[i]
        potMatch = arrayIndexRegex.match(part)
        if potMatch is None:
            # It is not an index in an array
            if part not in currLoc:
                if makeIdentifier:
                    currLoc[part] = {}
                else:
                    raise MissingIdentifierException(identifier)
            if (i == len(jsonParts) - 1):
                currLoc[part] = toWrite
            else:
                currLoc = currLoc.get(part)
        else:
            # it is an index in an array
            index = int(potMatch.group(1))
            # TODO make this line work so it could handle an array as the root
            if part[:potMatch.start()] not in currLoc:
                if makeIdentifier:
                    currLoc[part[:potMatch.start()]] = []
                else:
                    raise MissingIdentifierException(identifier)
            currLoc = currLoc.get(part[:potMatch.start()])
            if len(currLoc) <= index:
                raise MissingIdentifierException(identifier)
            while len(currLoc) <= index:
                currLoc.append({})
            if (i == len(jsonParts) - 1):
                currLoc[index] = toWrite
            else:
                currLoc = currLoc[index]

# end of JSON section


"""
A class that contains the data parse from marked code. It contains the identifier used in the code for the marked section,
the destination for the bit of marked code, the location in that destination to store it,
the code itself, the delimiter used in this source file and the location of the source file
"""


class MarkedCode:
    def __init__(self, originFile: str, destinationFile: str, destinationLocation: str, identifier: str, javascript: JSONizableCode, delimiter: str):
        self.__originFile = originFile
        self.__destFile = destinationFile
        self.__destLoc = destinationLocation
        self.__id = identifier
        self.__code = javascript
        self.__delimiter = delimiter

    def getOriginFile(self):
        return self.__originFile

    """
    Returns the canonical path to the original source file.
    If the path is not valid it returns None
    """

    def getCanonicalOriginFile(self):
        path = os.path.expanduser(self.__originFile)
        if os.path.exists(path):
            return os.path.realpath(path)
        else:
            return None

    def getDestinationFile(self):
        return self.__destFile

    """
    Returns the canonical path to the file of the json to store the code in
    If the path is not valid it returns None
    """

    def getCanonicalDestinationFile(self):
        # This adding of a slash might make things explode on Windows, who knows (should test)
        dirPart = os.path.dirname(self.__originFile) + "/"
        completePath = ""
        if os.path.isabs(os.path.expanduser(self.__destFile)):
            completePath = os.path.expanduser(self.__destFile)
        else:
            completePath = dirPart + self.__destFile
            completePath = os.path.abspath(completePath)
        if os.path.exists(completePath):
            return os.path.realpath(completePath)
        else:
            return None

    def getDestinationLocation(self):
        return self.__destLoc

    def getIdentifier(self):
        return self.__id

    def getDelimiter(self):
        return self.__delimiter

    """
    Returns the stored code as a JSONizableCode object
    """

    def getCode(self):
        return self.__code

    """
    Set the stored code. This object must be a JSONizableCode object
    """

    def setCode(self, code: JSONizableCode):
        self.__code = code

    """
    Writes the code back to the origin file.
    This function assumes that the file actually contains the marked code's identifiers
    """

    def writeToOrigin(self):
        startRegex = re.compile(
            '^.*' + self.__delimiter + '\\s*start\\s*:\\s*\'' + self.__id + '\'\\s*$')
        endRegex = re.compile(
            '^.*' + self.__delimiter + '\\s*end\\s*:\\s*\'' + self.__id + '\'\\s*$')
        origFile = open(self.__originFile, 'r')
        lines = origFile.readlines()
        origFile.close()
        # look for the index (line number) that matches the start position
        i = 0
        while i < len(lines) and startRegex.match(lines[i]) is None:
            i += 1
        startMarker = i
        # look for the index (line number) that matches the end position
        i += 1
        while i < len(lines) and endRegex.match(lines[i]) is None:
            i += 1
        endMarker = i
        # recreate the file with the contents between the first and last one
        fileContents = "".join(lines[:startMarker+1]) + \
            self.getCode().getCode() + "".join(lines[endMarker:])
        origFile = open(self.__originFile, 'w')
        origFile.write(fileContents)
        origFile.close()

    """
    Writes the contained data to a json object
    """

    def writeToJSON(self, jsonObj):
        writeToJSONIdentifier(jsonObj, self.getDestinationLocation(),
                              self.getCode().getJSONizedCode())


"""
A function that parses the first bit of code that is marked to be put in JSON
@throws MissingMarkingsException if a sort of marker/identifier was missing from the file: location, destination or end are missing
@param currFile: the file to parse from (the actual file and not the filename)
@param currFileName: the name of the file currently being parsed
@param delimiter: the delimiter which indicates the start of a comment meant to be parsed
@param toIgnore: an array of identifier to skip and not parse if encountered, if it is set to None
it will not skip any identifiers
@returns a tuple containing in the first position the MarkedCode object that was parsed and in the second
position the byte offset from the start of the file, if both are None no more marked code was found in this file
"""


def parseFileForSingleMarkedCode(currFile, currFileName: str, delimiter: str, toIgnore=None):
    if toIgnore is None:
        toIgnore = []
    fileRegex = re.compile('^.*' + delimiter +
                           '\\s*destination\\s*:\\s*\'([\\w\\-\\.]+)\'\\s*$')
    locationRegex = re.compile(
        '^.*' + delimiter + '\\s*location\\s*:\\s*\'([\\w\\-\\.]+)\'\\s*$')
    startRegex = re.compile(
        '^.*' + delimiter + '\\s*start\\s*:\\s*\'([\\w\\-\\.]+)\'\\s*$')
    endRegex = re.compile('^.*' + delimiter +
                          '\\s*end\\s*:\\s*\'([\\w\\-\\.]+)\'\\s*$')

    # attempt to find a start identifier
    currLine = currFile.readline()
    identifier = None
    while identifier is None:
        # attempt to find something that matches the start identifier regex
        while startRegex.match(currLine) is None:
            currLine = currFile.readline()
            # if we have reached the end of the file return that nothing was found
            if currLine == "":
                return None, None
        identifier = startRegex.match(currLine).group(1)
        # check if we need to skip this identifier
        if identifier in toIgnore:
            identifier = None

    postIDLocation = currFile.tell()
    # Read the lines and keep them until we hit the end identifier and take the first location and destination identifiers
    lines = []
    location = None
    destFile = None
    currLine = currFile.readline()
    while (endRegex.match(currLine) is None or endRegex.match(currLine).group(1) != identifier) and currLine != "":
        if (not locationRegex.match(currLine) is None) and location is None:
            location = locationRegex.match(currLine).group(1)
        elif (not fileRegex.match(currLine) is None) and destFile is None:
            destFile = fileRegex.match(currLine).group(1)
        lines.append(currLine)
        currLine = currFile.readline()
    # Add the bit that might not yet have been added because the line with end on it was not yet processed
    fin = endRegex.match(currLine)
    if (not fin is None) and (endRegex.match(currLine).group(1) == identifier):
        lines.append(currLine[:fin.start()])

    missingMarkers = []
    if location is None:
        missingMarkers.append("location")
    if destFile is None:
        missingMarkers.append("destination")
    if currLine == "":
        missingMarkers.append("end")

    if len(missingMarkers) > 0:
        raise MissingMarkingsException(missingMarkers, identifier)
    else:
        return MarkedCode(currFileName, destFile, location, identifier, JSONizableCode("".join(lines)), delimiter), postIDLocation


"""
Runs parseFileForSingleMarkedCode multiple times over the same file, making sure it does not parse the same identifier multiple times
@param fileName: the name of the file to parse
@param delimiter: the delimiter that indicates the start of a comment that needs to be parsed
"""


def parseFileForMarkedCode(fileName: str, delimiter: str):
    currFile = open(fileName, 'r')
    listMarkedCode = []
    parsedIdentifiers = []
    while True:
        try:
            result = parseFileForSingleMarkedCode(
                currFile, fileName, delimiter, parsedIdentifiers)
            if (result[0] is None) and (result[1] is None):
                break
            else:
                listMarkedCode.append(result[0])
                currFile.seek(result[1])
                parsedIdentifiers.append(result[0].getIdentifier())
        except MissingMarkingsException as err:
            identifier = err.getIdentifier()
            parsedIdentifiers.append(identifier)
            print("Errors while parsing " + identifier +
                  " in " + fileName, file=stderr)
            markers = err.getMissinMarkings()
            if "location" in markers:
                print("Missing the location identifier", file=stderr)
            if "destination" in markers:
                print("Missing the destination identifier", file=stderr)
            if "end" in markers:
                print("Missing the corresponding end identifier, did you misspell it?",
                      file=stderr)
    return listMarkedCode


"""
Retrieves all the filenames starting from a given file that have a given extension extension and returns them as a list
If the given filename is a directory it will recursively look through all it's directories and look for files that end with the extension
@param filename: the name of the file to start looking from
@param extension: the extension the files should have
@returns the list of all the filenames underneath the given filename that have the same extension as the given one
"""


def getAllFilenames(filename: str, extension: str):
    start = os.path.expanduser(filename)
    filesToHandle = []
    if os.path.isdir(start):
        for elemInDir in os.scandir(start):
            # go through each element recursively looking for filenames
            if elemInDir.is_dir():
                filesToHandle = filesToHandle + \
                    getAllFilenames(elemInDir.path, extension)
            else:
                if elemInDir.path.endswith(extension):
                    filesToHandle.append(elemInDir.path)
    elif start.endswith(extension):
        filesToHandle.append(start)
    return filesToHandle


"""
Gets all the marked code files with a given extension underneath a given location.
@param location: the location to start from and check underneath
@param extension: the extension that the source code files should have
@param delimiter: the delimiter that indicates a comment that needs to be parsed in the source code
"""


def getAllMarkedCode(location: str, extension: str, delimiter: str):
    # Get all the different files and parse them
    toWorkOn = getAllFilenames(location, extension)
    markedCode = []
    for fileName in toWorkOn:
        markedCode = markedCode + \
            parseFileForMarkedCode(fileName, delimiter)
    return markedCode


"""
Parse all the json objects from all the different destination files mentioned in the array of MarkedCode objects
@param markedCode: a list of markedCode objects from which to get the destinations to load
"""


def getAllReferencedJsonFiles(markedCode: list):
    destinationFiles = {}
    codeReferencingValidFiles = []
    for marked in markedCode:
        # try to get a canonical path for easy comparison in dict
        destFile = marked.getCanonicalDestinationFile()
        if not destFile is None:
            codeReferencingValidFiles.append(marked)
            # load json and insert if not yet present
            if destFile not in destinationFiles:
                jsonObj = loadJSONFromFile(destFile)
                destinationFiles[destFile] = jsonObj
            # add this marked code to the
        else:
            print("The file '" + marked.getOriginFile() + "' contains a reference to the file '" +
                  marked.getDestinationFile() + "', but '" + destFile + "' doe not exist.", file=stderr)
    return destinationFiles, codeReferencingValidFiles
