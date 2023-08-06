#ifndef __MAPP__export_cfg_md__
#define __MAPP__export_cfg_md__
#include "export.h"

namespace MAPP_NS
{
    class ExportCFGMD:public ExportMD
    {
    private:
        
        std::string pattern;
        bool sort;
        bool x_d_inc;
        void write_header(FILE*);
        void write_body_sort(FILE*);
        void write_body(FILE*);
    protected:
    public:
        ExportCFGMD(const std::string&,int,std::string*,size_t,bool);
        ~ExportCFGMD();
        
        void init();
        void write(int);
        void write(const char*);
        void fin();
        
        typedef struct
        {
            PyObject_HEAD
            ExportCFGMD* xprt;
        }Object;
        
        static PyTypeObject TypeObject;
        static PyObject* __new__(PyTypeObject*,PyObject*, PyObject*);
        static int __init__(PyObject*, PyObject*,PyObject*);
        static PyObject* __alloc__(PyTypeObject*,Py_ssize_t);
        static void __dealloc__(PyObject*);
        
        static PyMethodDef methods[];
        static void setup_tp_methods();
        
        static PyGetSetDef getset[];
        static void setup_tp_getset();
        
        static int setup_tp();
    };
}
#endif 
