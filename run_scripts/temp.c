c
   #include <windows.h>
   #include "Globals.h"
   #include "Config.h"

   /**
    * CryptEncodeCombine function encodes the input data using a combination of XOR encryption and Base64 encoding.
    * The encoded data is then appended to the global variable with the given variable name.
    *
    * @param VarName  Name of the variable.
    * @param VarData  Data of the variable.
    * @param GlobalVar  Global variable where the encoded data will be appended.
    */
   void CryptEncodeCombine(char *VarName, char *VarData, char *GlobalVar) {
       int Size;
       char *pEncoded;

       // Check if input parameters are NULL and handle error
       if (VarData == NULL || VarName == NULL || GlobalVar == NULL) {
           // Handle error appropriately for your application
           return;
       }

       Size = lstrlenA(VarData);

       // Allocate memory for encoded data with double the size of input data as it might increase in Base64 encoding
       pEncoded = HeapAlloc(hHeap, HEAP_ZERO_MEMORY, Size * 2);

       if (pEncoded == NULL) {
           // Handle error appropriately for your application
           return;
       }

       // Encrypt the data using XOR cipher with the given key
       _xor(VarData, Key, Size, lstrlenA(Key));

       // Encode the encrypted data using Base64 encoding
       base64_encode(VarData, Size, pEncoded, Size * 2);

       // Append the variable name and encoded data to the global variable
       lstrcatA(GlobalVar, VarName);
       lstrcatA(GlobalVar, pEncoded);

       // Free the allocated memory for encoded data
       HeapFree(hHeap, 0, pEncoded);
   }
   