1. The File Container: XML Property List
The .gmd file is actually an Apple Property List (plist) in XML format.
Structure: Key-value pairs wrapped in <dict>.
Keys (<k>): The identifiers.
Values: Can be Strings (<s>), Integers (<i>), or Booleans (<t/> for true, <f/> for false).
The Critical Keys:
You need to parse the XML and extract the content of these specific keys:
k4: The Level Data String. This is the payload you need to decode.
k2: The Level Name (Raw string).
k3: The Level Description (Base64 encoded string, not URL-safe, just standard Base64).
2. The Decoding Pipeline (The "Level String")
The string found inside k4 is the result of a specific compression pipeline. To get the readable data, you must reverse these steps exactly.
Step A: Base64 Decoding (URL-Safe)
The raw string is Base64, but RobTop (the developer) uses a URL-safe variant.
Replacement: You must replace all instances of - with + and _ with /.
Padding: Base64 strings must have a length divisible by 4. If length % 4 != 0, append = characters to the end until it is.
Decode: Convert the resulting string into a byte array.
Step B: Gzip Decompression
The byte array resulting from Step A is a Gzip compressed stream.
Header Check: Valid Gzip streams usually start with the bytes 0x1F 0x8B.
Algorithm: Use your language's standard Gzip or Zlib library (e.g., zlib in C++/Python, GZipStream in C#) to decompress the bytes into a UTF-8 string.
(Note: In savedata files like CCLocalLevels.dat, there is an XOR encryption step before Gzip. In .gmd export files, this is usually skipped. If you get garbage data after Base64 decoding, try XORing the bytes with the key 11 before decompressing.)
3. The Data Schema (The Decompressed String)
Once decompressed, you have a massive ASCII string. This is a custom delimiter-based format.
High-Level Structure
code
Text
HeaderString;ObjectString;ObjectString;ObjectString;...
Delimiter: Semicolon ;
Part 0 (Header): The first segment defines level-wide settings (Background, Song, Speed, Mode).
Parts 1..N (Objects): Every subsequent segment represents a specific game object.
Low-Level Structure (Object/Header Syntax)
Inside the Header or an Object, data is stored as a flat list of Key-Value pairs separated by commas.
code
Text
Key,Value,Key,Value,Key,Value
Key: An integer representing the property type (e.g., 1 is ID, 2 is X-pos).
Value: The data for that property.
Parsing Logic: You must iterate through the string splitting by ,, taking items in steps of 2. Array[i] is the Key, Array[i+1] is the Value.
4. Property Mapping (The "Rosetta Stone")
To make your code useable, you need a dictionary to map the numeric Keys to variable names.
Universal Object Properties
Key	Type	Description
1	Int	Object ID (Determines if it's a block, spike, ship portal, etc.)
2	Float	X Position (1 block = 30 units)
3	Float	Y Position (1 block = 30 units)
4	Bool	Flip Horizontally (1 = True, 0 or missing = False)
5	Bool	Flip Vertically
6	Float	Rotation (Degrees)
32	Float	Scale (1.0 is default)
57	Int[]	Groups (Period separated string, e.g., 1.5.10)
20	Int	Editor Layer 1
25	Int	Z Order (Draw order)
Color & Trigger Properties
Key	Type	Description
7	Int	Red (0-255)
8	Int	Green (0-255)
9	Int	Blue (0-255)
10	Float	Duration (For triggers)
11	Bool	Touch Trigger
21	Int	Color ID (For objects that use palette colors)
Header Specific Properties (The first segment)
Key	Type	Description
kA1	Int	Game Mode (0=Cube, 1=Ship, etc.)
kA2	Int	Game Speed (0=Slow, 1=Normal, 2=Fast, etc.)
kA6	Int	Background ID
kA13	Int	Music Offset
5. Implementation Logic: The "Builder"
When rewriting the file (serializing), you must adhere to strict formatting rules or the game will crash/fail to load.
Float formatting:
GD hates trailing decimals on whole numbers.
Correct: 30
Crash/Bug risk: 30.0
You must strip .0 from floats during string construction.
Booleans:
True must be written as "1".
False is usually handled by simply omitting the key entirely to save space, but "0" is acceptable.
Group IDs (57):
If an object is in multiple groups, they are stored as a string separated by dots: 1.20.99.
Re-Encoding Pipeline:
Join properties with ,.
Join objects with ;.
Append a trailing semicolon ; at the very end of the string.
Gzip compress the string.
Base64 Encode the binary result.
Replace + -> - and / -> _.
6. Summary for Your Project
If you are writing this in C#, C++, or Java, your architecture should look like this:
GMDParser Class:
Input: File or String.
Method: ExtractLevelString() (XML parsing).
Method: Decode() (Base64 -> Gzip -> String).
Method: ParseObjects() (String split logic).
Output: List<GameObject>.
GameObject Class:
Properties: ID, X, Y, Rotation, etc.
Method: ToString() (Converts self back to 1,XX,2,YY...).
GMDBuilder Class:
Input: List<GameObject>.
Method: BuildLevelString() (Joins objects, Gzips, Base64s).
Method: Export() (Wraps result in the XML k4 tag and saves file).