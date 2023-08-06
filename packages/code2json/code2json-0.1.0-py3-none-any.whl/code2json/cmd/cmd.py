from ..code2json import getAllMarkedCode, getAllReferencedJsonFiles, writeJSONToFile, getFromJSONIdentifier, MissingIdentifierException, JSONizableCode
from argparse import ArgumentParser
import os
from sys import stderr

VERSION = "0.1.0"

# TODO check that it could handle a case where the root is an array and not a dictionary
# TODO add a safe option that takes a backup of the code or JSON it is writing to
# TODO add a verbose mode that makes it print way more

"""
Executes the writing of the given source code to the given json files.
First it writes to all the JSON objects and then writes those objects back to their files
@param markedCode: a list of MarkedCode objects that describe a bit of marked up code 
that needs to be written to one of the JSON objects. If it has a location that does not yet
exist in the JSON it will create that location
@param jsonDict: a dictionary the maps a canonical path to the corresponding JSON object
"""


def executeCode2json(markedCode: list, jsonDict: dict):
    # write all the code to json
    for marked in markedCode:
        destFile = marked.getCanonicalDestinationFile()
        jsonObj = jsonDict[destFile]
        marked.writeToJSON(jsonObj)
    print("Writing modified JSON back to file")
    # write json to file
    for path in jsonDict:
        writeJSONToFile(jsonDict[path], path)


"""
Executes the writing to the given source code from the given json files.
First it reads from all the JSON objects and writes that to the code. 
Then writes the all the marked bits of code back to their files
@param markedCode: a list of MarkedCode objects that describe a bit of marked up code 
that needs to be written to with the content of the JSON objects. If it has a location that does not yet
exist in the JSON it will print an error and move on to the next one
@param jsonDict: a dictionary the maps a canonical path to the corresponding JSON object
"""


def executeJson2code(markedCode: list, jsonDict: dict):
    changedCode = []
    for marked in markedCode:
        destFile = marked.getCanonicalDestinationFile()
        jsonObj = jsonDict[destFile]

        try:
            JsonSource = getFromJSONIdentifier(
                jsonObj, marked.getDestinationLocation())
            if type(JsonSource) is str:
                marked.setCode(JSONizableCode.loadFromJSON(JsonSource))
                changedCode.append(marked)
            else:
                print("The object in the identifier'" +
                      marked.getDestinationLocation() + "' in the JSON file '" + destFile + "' was not a string and will not be written to the source file '" + marked.getOriginFile() + "'", file=stderr)
        except MissingIdentifierException as err:
            print("Encountered an invalid identifier ('" +
                  err.getIdentifier() + "') when attempting to read from the JSON file '" + destFile + "' to get source code for the source file '" + marked.getOriginFile() + "'", file=stderr)

    for marked in changedCode:
        marked.writeToOrigin()


"""
This is the main function that builds a parser and parses the given command.
Then it looks for all the marked code mentioned in the command and parses it.
Next is actually executes the required function (aka 'write to code' or 'write to JSON')
"""


def main():
    parser = ArgumentParser(description="Easily insert JavaScript into JSON and extract it from JSON",
                            prog="code2json")
    parser.add_argument('location', type=str,
                        help="The location from where to run the insertion. This can be a file or directory. This will be the location of the javascript files, not the JSON files")
    parser.add_argument('extension', type=str,
                        help="The extension of all source code files that need to be handled.")
    parser.add_argument('mode', type=str, choices={"2code", "2json"},
                        help="The mode in which to run js2json. Either '2code' or '2json'")
    parser.add_argument('-d', '--delimiter', type=str, dest='delimiter', default="//",
                        help="The delimiter of that indicates a comment. The default is //")
    parser.add_argument("--version", action='version',
                        version="%(prog)s " + VERSION)
    args = parser.parse_args()

    if args.mode == "2code" or args.mode == "2json":
        # get all the different files to insert into and parse those
        print("Parsing source code files")
        markedCode = getAllMarkedCode(
            args.location, args.extension, args.delimiter)
        if len(markedCode) == 0:
            print("No file found that contained valid markings. Stopping.")
            return
        # Store them in a dictionary so we don't load the same json twice
        print("Loading all the referenced JSON files")
        pathToJsonDict, markedCode = getAllReferencedJsonFiles(markedCode)

        if args.mode == "2code":
            executeJson2code(markedCode, pathToJsonDict)
        elif args.mode == "2json":
            executeCode2json(markedCode, pathToJsonDict)
    else:
        print(args.mode +
              " was given as the mode, but this does not seem to be implemented")


if __name__ == "__main__":
    main()
