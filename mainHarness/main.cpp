#include <stdio.h>
#include <comdef.h>
#include <windows.h>
#include <t2embapi.h>
#include <XpsObjectModel.h>
#include <XpsPrint.h>
#include <iostream>
#include <atlbase.h>
using namespace std;
#pragma comment(lib, "XpsPrint.lib")
#pragma warning(disable : 4995)
#pragma warning(disable : 4996)
#pragma warning(disable : 4100)
// The font to use for the page text.  Needs to be a TrueType font.

// This function creates a font resource for the given font name with the 
// embedding type set appropriately for the licensing intent of the font.
extern "C" __declspec(dllexport) int fuzzme(wchar_t* filename);
void Usage(wchar_t* argv0)
{
    fwprintf(stderr, L"XPS Object Model Printing Sample\n\n");
    fwprintf(stderr, L"\tUsage: %s <printer name> [<output file name>]\n", argv0);
}

wchar_t* charToWChar(const char* text)
{
    size_t size = strlen(text) + 1;
    wchar_t* wa = new wchar_t[size];
    mbstowcs(wa, text, size);
    return wa;
}

int fuzzme(wchar_t* filename)
{
    HRESULT hr = S_OK;
    HANDLE completionEvent = NULL;
    IXpsPrintJob* job = NULL;
    IXpsPrintJobStream* jobStream = NULL;
    IXpsOMObjectFactory* xpsFactory = NULL;
    XPS_JOB_STATUS jobStatus = {};

    int a;

    if (SUCCEEDED(hr))
    {
        completionEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
        if (!completionEvent)
        {
            hr = HRESULT_FROM_WIN32(GetLastError());
            fwprintf(stderr, L"ERROR: Could not create competion event: %08X\n", hr);
        }
    }


    char pszName[L_tmpnam] = { '\0' };
    tmpnam_s(pszName);


    if (SUCCEEDED(hr))
    {
        if (FAILED(hr = StartXpsPrintJob(
            TEXT("PS"),  //
            NULL,                       //jobName
            NULL,                       //outputFileName
            NULL,                       //progressEvent     
            completionEvent,            //completionEvent   
            NULL,                       //printablePagesOn  
            0,                          //printablePagesOnCount
            &job,                       //xpsPrintJob       
            &jobStream,                 //documentStream   
            NULL                        //printTicketStream Ticket
        )))
        {
            fwprintf(stderr, L"ERROR: Could not start XPS print job: %08X\n", hr);
        }
    }


    //XPS OM Object Factory
    if (SUCCEEDED(hr))
    {
        if (FAILED(hr = CoCreateInstance(
            __uuidof(XpsOMObjectFactory),
            NULL,
            CLSCTX_INPROC_SERVER, //CLSCTX enumeration
            __uuidof(IXpsOMObjectFactory),
            reinterpret_cast<void**>(&xpsFactory)
        )
        )
            )
        {
            fwprintf(stderr, L"ERROR: Could not create XPS OM Object Factory: %08X\n", hr);
        }
    }


    IStream* pStream;
    hr = SHCreateStreamOnFileEx(filename, STGM_READ, FILE_ATTRIBUTE_NORMAL, FALSE, NULL, (IStream**)&pStream);
    if (FAILED(hr))
    {
        cout << "SHCreateStreamOnFileEx fail" << hex << hr << endl;
        return 0;
    };

    char content[100000] = { 0 };
    ULONG readEd = 0;
    ULONG writeEd = 0;
    //buf
    pStream->Read(content, 100000, &readEd);
    hr = jobStream->Write(content, readEd, &writeEd); //IStreamOverWritePrinter::Write
    int count = 0;
    count += writeEd;//1024,

    while (readEd != 0)
    {
        memset(content, 0, 100000);
        pStream->Read(content, 100000, &readEd);
        jobStream->Write(content, readEd, &writeEd);
        count += writeEd;
    }

    if (SUCCEEDED(hr))
    {
        if (FAILED(hr = jobStream->Close()))
        {
            fwprintf(stderr, L"ERROR: Could not close job stream: %08X\n", hr);
        }
    }
    else
    {
        // Only cancel the job if we succeeded in creating one in the first place.
        if (job)
        {
            // Tell the XPS Print API that we're giving up.  Don't overwrite hr with the return from
            // this function.
            job->Cancel();
        }
    }

    if (SUCCEEDED(hr))
    {
        wprintf(L"Waiting for job completion...\n");

        if (WaitForSingleObject(completionEvent, INFINITE) != WAIT_OBJECT_0)
        {
            hr = HRESULT_FROM_WIN32(GetLastError());
            fwprintf(stderr, L"ERROR: Wait for completion event failed: %08X\n", hr);
        }
    }

    if (SUCCEEDED(hr))
    {
        if (FAILED(hr = job->GetJobStatus(&jobStatus)))
        {
            fwprintf(stderr, L"ERROR: Could not get job status: %08X\n", hr);
        }
    }

    if (SUCCEEDED(hr))
    {
        switch (jobStatus.completion)
        {
        case XPS_JOB_COMPLETED:
            break;
        case XPS_JOB_CANCELLED:
            fwprintf(stderr, L"ERROR: job was cancelled\n");
            hr = E_FAIL;
            break;
        case XPS_JOB_FAILED:
            fwprintf(stderr, L"ERROR: Print job failed: %08X\n", jobStatus.jobStatus);
            hr = E_FAIL;
            break;
        default:
            fwprintf(stderr, L"ERROR: unexpected failure\n");
            hr = E_UNEXPECTED;
            break;
        }
    }

    if (SUCCEEDED(hr))
    {
        wprintf(L"Done!\n");
    }

    if (xpsFactory)
    {
        xpsFactory->Release();
        xpsFactory = NULL;
    }

    if (jobStream)
    {
        jobStream->Release();
        jobStream = NULL;
    }

    if (job)
    {
        job->Release();
        job = NULL;
    }

    if (completionEvent)
    {
        CloseHandle(completionEvent);
        completionEvent = NULL;
    }

    CoUninitialize();

    return SUCCEEDED(hr) ? 0 : 1;
}
int wmain(int argc, wchar_t* argv[])
{

    //COM
    HRESULT hr = S_OK;
    if (FAILED(hr = CoInitializeEx(0, COINIT_MULTITHREADED)))
    {
        fwprintf(stderr, L"ERROR: CoInitializeEx failed with HRESULT 0x%X\n", hr);
        return 1;
    }
    fuzzme(argv[1]);
}
