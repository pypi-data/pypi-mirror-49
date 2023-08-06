(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
module.exports=[
    {
        "name": "reserved0",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved1",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved2",
        "args": [],
        "ret": null
    },
    {
        "name": "DestroyJavaVM",
        "args": [
            "JavaVM*"
        ],
        "ret": "jint"
    },
    {
        "name": "AttachCurrentThread",
        "args": [
            "JavaVM*",
            "void**",
            "void*"
        ],
        "ret": "jint"
    },
    {
        "name": "DetachCurrentThread",
        "args": [
            "JavaVM*"
        ],
        "ret": "jint"
    },
    {
        "name": "GetEnv",
        "args": [
            "JavaVM*",
            "void**",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "AttachCurrentThreadAsDaemon",
        "args": [
            "JavaVM*",
            "void**",
            "void*"
        ],
        "ret": "jint"
    },
]

},{}],2:[function(require,module,exports){
module.exports=[
    {
        "name": "reserved0",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved1",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved2",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved3",
        "args": [],
        "ret": null
    },
    {
        "name": "GetVersion",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jint"
    },
    {
        "name": "DefineClass",
        "args": [
            "JNIEnv*",
            "char*",
            "jobject",
            "jbyte*",
            "jsize"
        ],
        "ret": "jclass"
    },
    {
        "name": "FindClass",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "jclass"
    },
    {
        "name": "FromReflectedMethod",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "FromReflectedField",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "ToReflectedMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jboolean"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetSuperclass",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jclass"
    },
    {
        "name": "IsAssignableFrom",
        "args": [
            "JNIEnv*",
            "jclass",
            "jclass"
        ],
        "ret": "jboolean"
    },
    {
        "name": "ToReflectedField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jboolean"
        ],
        "ret": "jobject"
    },
    {
        "name": "Throw",
        "args": [
            "JNIEnv*",
            "jthrowable"
        ],
        "ret": "jint"
    },
    {
        "name": "ThrowNew",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*"
        ],
        "ret": "jint"
    },
    {
        "name": "ExceptionOccurred",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jthrowable"
    },
    {
        "name": "ExceptionDescribe",
        "args": [
            "JNIEnv*"
        ],
        "ret": "void"
    },
    {
        "name": "ExceptionClear",
        "args": [
            "JNIEnv*"
        ],
        "ret": "void"
    },
    {
        "name": "FatalError",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "PushLocalFrame",
        "args": [
            "JNIEnv*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "PopLocalFrame",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "DeleteGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "DeleteLocalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "IsSameObject",
        "args": [
            "JNIEnv*",
            "jobject",
            "jobject"
        ],
        "ret": "jboolean"
    },
    {
        "name": "NewLocalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "EnsureLocalCapacity",
        "args": [
            "JNIEnv*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "AllocObject",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObject",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObjectV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObjectA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetObjectClass",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jclass"
    },
    {
        "name": "IsInstanceOf",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetMethodID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "CallObjectMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallObjectMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallObjectMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallBooleanMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallByteMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallByteMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallByteMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallCharMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallCharMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallCharMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallShortMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallShortMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallShortMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallIntMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallIntMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallIntMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallLongMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallLongMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallLongMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallFloatMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallFloatMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallFloatMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallDoubleMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallVoidMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallVoidMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallVoidMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualObjectMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualObjectMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualObjectMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualBooleanMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualByteMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualByteMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualByteMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualCharMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualCharMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualCharMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualShortMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualShortMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualShortMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualIntMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualIntMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualIntMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualLongMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualLongMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualLongMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualFloatMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualFloatMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualFloatMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualDoubleMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualVoidMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualVoidMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualVoidMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "GetFieldID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "GetObjectField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetBooleanField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetByteField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetCharField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetShortField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetIntField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jint"
    },
    {
        "name": "GetLongField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetFloatField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetDoubleField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jdouble"
    },
    {
        "name": "SetObjectField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "SetBooleanField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jboolean"
        ],
        "ret": "void"
    },
    {
        "name": "SetByteField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jbyte"
        ],
        "ret": "void"
    },
    {
        "name": "SetCharField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jchar"
        ],
        "ret": "void"
    },
    {
        "name": "SetShortField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jshort"
        ],
        "ret": "void"
    },
    {
        "name": "SetIntField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "SetLongField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jlong"
        ],
        "ret": "void"
    },
    {
        "name": "SetFloatField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jfloat"
        ],
        "ret": "void"
    },
    {
        "name": "SetDoubleField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jdouble"
        ],
        "ret": "void"
    },
    {
        "name": "GetStaticMethodID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "CallStaticObjectMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticObjectMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticObjectMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticBooleanMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticByteMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticByteMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticByteMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticCharMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticCharMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticCharMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticShortMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticShortMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticShortMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticIntMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticIntMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticIntMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticLongMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticLongMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticLongMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticFloatMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticFloatMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticFloatMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticDoubleMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticVoidMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallStaticVoidMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallStaticVoidMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "GetStaticFieldID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "GetStaticObjectField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetStaticBooleanField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetStaticByteField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetStaticCharField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetStaticShortField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetStaticIntField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jint"
    },
    {
        "name": "GetStaticLongField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetStaticFloatField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetStaticDoubleField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jdouble"
    },
    {
        "name": "SetStaticObjectField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticBooleanField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jboolean"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticByteField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jbyte"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticCharField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jchar"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticShortField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jshort"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticIntField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticLongField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jlong"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticFloatField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jfloat"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticDoubleField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jdouble"
        ],
        "ret": "void"
    },
    {
        "name": "NewString",
        "args": [
            "JNIEnv*",
            "jchar*",
            "jsize"
        ],
        "ret": "jstring"
    },
    {
        "name": "GetStringLength",
        "args": [
            "JNIEnv*",
            "jstring"
        ],
        "ret": "jsize"
    },
    {
        "name": "GetStringChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "ReleaseStringChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "NewStringUTF",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "jstring"
    },
    {
        "name": "GetStringUTFLength",
        "args": [
            "JNIEnv*",
            "jstring"
        ],
        "ret": "jsize"
    },
    {
        "name": "GetStringUTFChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "char*"
    },
    {
        "name": "ReleaseStringUTFChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "GetArrayLength",
        "args": [
            "JNIEnv*",
            "jarray"
        ],
        "ret": "jsize"
    },
    {
        "name": "NewObjectArray",
        "args": [
            "JNIEnv*",
            "jsize",
            "jclass",
            "jobject"
        ],
        "ret": "jobjectArray"
    },
    {
        "name": "GetObjectArrayElement",
        "args": [
            "JNIEnv*",
            "jobjectArray",
            "jsize"
        ],
        "ret": "jobject"
    },
    {
        "name": "SetObjectArrayElement",
        "args": [
            "JNIEnv*",
            "jobjectArray",
            "jsize",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "NewBooleanArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jbooleanArray"
    },
    {
        "name": "NewByteArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jbyteArray"
    },
    {
        "name": "NewCharArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jcharArray"
    },
    {
        "name": "NewShortArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jshortArray"
    },
    {
        "name": "NewIntArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jintArray"
    },
    {
        "name": "NewLongArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jlongArray"
    },
    {
        "name": "NewFloatArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jfloatArray"
    },
    {
        "name": "NewDoubleArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jdoubleArray"
    },
    {
        "name": "GetBooleanArrayElements",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jboolean*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetByteArrayElements",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jboolean*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetCharArrayElements",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetShortArrayElements",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jboolean*"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetIntArrayElements",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jboolean*"
        ],
        "ret": "jint"
    },
    {
        "name": "GetLongArrayElements",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jboolean*"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetFloatArrayElements",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jboolean*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetDoubleArrayElements",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jboolean*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "ReleaseBooleanArrayElements",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jboolean*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseByteArrayElements",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jbyte*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseCharArrayElements",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jchar*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseShortArrayElements",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jshort*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseIntArrayElements",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jint*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseLongArrayElements",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jlong*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseFloatArrayElements",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jfloat*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseDoubleArrayElements",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jdouble*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "GetBooleanArrayRegion",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jsize",
            "jsize",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "GetByteArrayRegion",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jsize",
            "jsize",
            "jbyte*"
        ],
        "ret": "void"
    },
    {
        "name": "GetCharArrayRegion",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "GetShortArrayRegion",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jsize",
            "jsize",
            "jshort*"
        ],
        "ret": "void"
    },
    {
        "name": "GetIntArrayRegion",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jsize",
            "jsize",
            "jint*"
        ],
        "ret": "void"
    },
    {
        "name": "GetLongArrayRegion",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jsize",
            "jsize",
            "jlong*"
        ],
        "ret": "void"
    },
    {
        "name": "GetFloatArrayRegion",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jsize",
            "jsize",
            "jfloat*"
        ],
        "ret": "void"
    },
    {
        "name": "GetDoubleArrayRegion",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jsize",
            "jsize",
            "jdouble*"
        ],
        "ret": "void"
    },
    {
        "name": "SetBooleanArrayRegion",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jsize",
            "jsize",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "SetByteArrayRegion",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jsize",
            "jsize",
            "jbyte*"
        ],
        "ret": "void"
    },
    {
        "name": "SetCharArrayRegion",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "SetShortArrayRegion",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jsize",
            "jsize",
            "jshort*"
        ],
        "ret": "void"
    },
    {
        "name": "SetIntArrayRegion",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jsize",
            "jsize",
            "jint*"
        ],
        "ret": "void"
    },
    {
        "name": "SetLongArrayRegion",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jsize",
            "jsize",
            "jlong*"
        ],
        "ret": "void"
    },
    {
        "name": "SetFloatArrayRegion",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jsize",
            "jsize",
            "jfloat*"
        ],
        "ret": "void"
    },
    {
        "name": "SetDoubleArrayRegion",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jsize",
            "jsize",
            "jdouble*"
        ],
        "ret": "void"
    },
    {
        "name": "RegisterNatives",
        "args": [
            "JNIEnv*",
            "jclass",
            "JNINativeMethod*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "UnregisterNatives",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jint"
    },
    {
        "name": "MonitorEnter",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jint"
    },
    {
        "name": "MonitorExit",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jint"
    },
    {
        "name": "GetJavaVM",
        "args": [
            "JNIEnv*",
            "JavaVM**"
        ],
        "ret": "jint"
    },
    {
        "name": "GetStringRegion",
        "args": [
            "JNIEnv*",
            "jstring",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "GetStringUTFRegion",
        "args": [
            "JNIEnv*",
            "jstring",
            "jsize",
            "jsize",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "GetPrimitiveArrayCritical",
        "args": [
            "JNIEnv*",
            "jarray",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "ReleasePrimitiveArrayCritical",
        "args": [
            "JNIEnv*",
            "jarray",
            "void*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "GetStringCritical",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "ReleaseStringCritical",
        "args": [
            "JNIEnv*",
            "jstring",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "NewWeakGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jweak"
    },
    {
        "name": "DeleteWeakGlobalRef",
        "args": [
            "JNIEnv*",
            "jweak"
        ],
        "ret": "void"
    },
    {
        "name": "ExceptionCheck",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "NewDirectByteBuffer",
        "args": [
            "JNIEnv*",
            "void*",
            "jlong"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetDirectBufferAddress",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "GetDirectBufferCapacity",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetObjectRefType",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobjectRefType"
    }
]

},{}],3:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

var Types = require("../../utils/types");

function JNIEnvInterceptorARM64(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.vaList = NULL;
  this.vaListOffset = 0;
}

var keepforever;
JNIEnvInterceptorARM64.prototype = new JNIEnvInterceptor();

JNIEnvInterceptorARM64.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  //text = Memory.alloc(Process.pageSize);
  Memory.writePointer(text.add(0x400), parser);
  keepforever = text;
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new Arm64Writer(code, {
      pc: text
    }); // adrp x0, #0

    cw.putInstruction(0x90000000); // back up all registers - just to be safe

    for (var i = 1; i < 31; i++) {
      var ins = 0xF9000000; // src reg

      ins += i;
      var offset = 0x408 + i * Process.pointerSize; // dst address

      ins += offset / 2 << 8; // str x<n>, [x0, #<offset>]

      cw.putInstruction(ins);
    } // ldr x0, [x0, #0x400]


    cw.putInstruction(0xF9420000); // blr x0

    cw.putInstruction(0xD63F0000);
    cw.putPushRegReg("x0", "sp"); // adrp x0, #0

    cw.putInstruction(0x90000000); // restore all registers - apart from lr and sp

    for (var i = 1; i < 30; i++) {
      var ins = 0xF9400000; // src reg

      ins += i;
      var offset = 0x408 + i * Process.pointerSize; // dst address

      ins += offset / 2 << 8; // ldr x<n>, [x0, #<offset>]

      cw.putInstruction(ins);
    }

    cw.putPopRegReg("x0", "sp"); // blr x0

    cw.putInstruction(0xD63F0000); // adrp x1, #0

    cw.putInstruction(0x90000001); // ldr x2, [x1, #0x4f8]

    cw.putInstruction(0xF9427C22); // br x2

    cw.putInstruction(0xD61F0040);
    cw.flush();
  }); // required to prevent a crash

  Interceptor.attach(text, function () {});
};

JNIEnvInterceptorARM64.prototype.setUpVaListArgExtract = function (vaList) {
  this.stack = Memory.readPointer(vaList);
  this.stackIndex = 0;
  this.grTop = Memory.readPointer(vaList.add(Process.pointerSize));
  this.vrTop = Memory.readPointer(vaList.add(Process.pointerSize * 2));
  this.grOffs = Memory.readS32(vaList.add(Process.pointerSize * 3));
  this.grOffsIndex = 0;
  this.vrOffs = Memory.readS32(vaList.add(Process.pointerSize * 3 + 4));
  this.vrOffsIndex = 0;
};

JNIEnvInterceptorARM64.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = NULL;

  if (method.params[paramId] === "float" || method.params[paramId] === "double") {
    if (this.vrOffsIndex < 8) {
      currentPtr = this.vrTop.add(this.vrOffs).add(this.vrOffsIndex * Process.pointerSize * 2);
      this.vrOffsIndex++;
    } else {
      currentPtr = this.stack.add(this.stackIndex * Process.pointerSize);
      this.stackIndex++;
    }
  } else {
    if (this.grOffsIndex < 4) {
      currentPtr = this.grTop.add(this.grOffs).add(this.grOffsIndex * Process.pointerSize);
      this.grOffsIndex++;
    } else {
      currentPtr = this.stack.add(this.stackIndex * Process.pointerSize);
      this.stackIndex++;
    }
  }

  return currentPtr;
};

JNIEnvInterceptorARM64.prototype.resetVaListArgExtract = function () {
  this.stack = NULL;
  this.stackIndex = 0;
  this.grTop = NULL;
  this.vrTop = NULL;
  this.grOffs = NULL;
  this.grOffsIndex = 0;
  this.vrOffs = NULL;
  this.vrOffsIndex = 0;
};

JNIEnvInterceptorARM64.prototype.processVaListRetVal = function (retType, retval, registers) {
  return retval;
};

module.exports = JNIEnvInterceptorARM64;

},{"../../utils/types":14,"../jni_env_interceptor":6}],4:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

var Types = require("../../utils/types");

function JNIEnvInterceptorARM(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.vaList = NULL;
  this.vaListOffset = 0;
}

JNIEnvInterceptorARM.prototype = new JNIEnvInterceptor();

JNIEnvInterceptorARM.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  Memory.writePointer(text.add(0x400), parser);
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new ArmWriter(code, {
      pc: text
    });
    var dataOffset = 0; // str r0, [pc, #0x400]

    cw.putInstruction(0xe58f0400); // str r1, [pc, #0x400]

    cw.putInstruction(0xe58f1400); // str r2, [pc, #0x400]

    cw.putInstruction(0xe58f2400); // str r3, [pc, #0x400]

    cw.putInstruction(0xe58f3400); // str lr, [pc, #0x400]

    cw.putInstruction(0xe58fe400); // ldr r0, [pc, #0x3e4]

    cw.putInstruction(0xe59f03e4); // blx r0

    cw.putInstruction(0xe12fff30); // ldr r1, [pc, 0x3e0]

    cw.putInstruction(0xe59f13e8); // ldr r2, [pc, 0x3e0]

    cw.putInstruction(0xe59f23e8); // ldr r3, [pc, 0x3e0]

    cw.putInstruction(0xe59f33e8); //blx r0

    cw.putInstruction(0xe12fff30); // ldr r1, [pc, #0x3e4]

    cw.putInstruction(0xe59f13e4); // bx r1

    cw.putInstruction(0xe12fff11);
    cw.flush();
  }); // required to prevent a crash

  Interceptor.attach(text.add(56), function () {});
};

JNIEnvInterceptorARM.prototype.setUpVaListArgExtract = function (vaList) {
  this.vaList = vaList;
  this.vaListOffset = 0;
};

JNIEnvInterceptorARM.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = this.vaList.add(this.vaListOffset);
  this.vaListOffset += Types.sizeOf(method.params[paramId]);
  return currentPtr;
};

JNIEnvInterceptorARM.prototype.resetVaListArgExtract = function () {
  this.vaList = NULL;
  this.vaListOffset = 0;
};

JNIEnvInterceptorARM.prototype.processVaListRetVal = function (retType, retval, registers) {
  if (retType === "double" || retType === "int64") {
    retval = registers.r1.toString().substring(2) + registers.r0.toString().substring(2);
  }

  return retval;
};

module.exports = JNIEnvInterceptorARM;

},{"../../utils/types":14,"../jni_env_interceptor":6}],5:[function(require,module,exports){
var JAVA_VM_METHODS = require("../data/java_vm.json");

var Types = require("../utils/types");

function JavaVMInterceptor(references, threads, jniEnvInterceptor) {
  this.references = references;
  this.threads = threads;
  this.jniEnvInterceptor = jniEnvInterceptor;
  this.shadowJavaVM = NULL;
}

JavaVMInterceptor.prototype.isInitialised = function () {
  return !this.shadowJavaVM.isNull();
};

JavaVMInterceptor.prototype.get = function () {
  return this.shadowJavaVM;
};

JavaVMInterceptor.prototype.createJavaVMIntercept = function (id, methodAddr) {
  var self = this;
  var method = JAVA_VM_METHODS[id];
  var fridaArgs = [];

  for (var j = 0; j < method.args.length; j++) {
    var ftype = Types.convertNativeJTypeToFridaType(method.args[j]);
    fridaArgs.push(ftype);
  }

  var fridaRet = Types.convertNativeJTypeToFridaType(method.ret);
  var nativeFunction = new NativeFunction(methodAddr, fridaRet, fridaArgs);
  var nativeCallback = new NativeCallback(function () {
    var threadId = Process.getCurrentThreadId();
    var localArgs = [].slice.call(arguments);
    var javaVM = self.threads.getJavaVM();
    var jniEnv = NULL;
    localArgs[0] = javaVM;
    var ret = nativeFunction.apply(null, localArgs);

    if (method.name === "GetEnv" || method.name === "AttachCurrentThread" || method.name === "AttachCurrentThreadAsDaemon") {
      if (ret === 0) {
        self.threads.setJNIEnv(threadId, Memory.readPointer(localArgs[1]));
      }

      if (!self.jniEnvInterceptor.isInitialised()) {
        jniEnv = self.jniEnvInterceptor.create();
      } else {
        jniEnv = self.jniEnvInterceptor.get();
      }

      Memory.writePointer(localArgs[1], jniEnv);
    }

    return ret;
  }, fridaRet, fridaArgs);
  this.references.add(nativeCallback);
  return nativeCallback;
};

JavaVMInterceptor.prototype.create = function () {
  var javaVMOffset = 3;
  var javaVMLength = 8;
  var threadId = Process.getCurrentThreadId();
  var javaVM = this.threads.getJavaVM(threadId);
  var newJavaVMStruct = Memory.alloc(Process.pointerSize * javaVMLength);
  this.references.add(newJavaVMStruct);
  var newJavaVM = Memory.alloc(Process.pointerSize);
  Memory.writePointer(newJavaVM, newJavaVMStruct);

  for (var i = javaVMOffset; i < javaVMLength; i++) {
    var offset = i * Process.pointerSize;
    var javaVMStruct = Memory.readPointer(javaVM);
    var methodAddr = Memory.readPointer(javaVMStruct.add(offset));
    var callback = this.createJavaVMIntercept(i, ptr(methodAddr));
    Memory.writePointer(newJavaVMStruct.add(offset), callback);
  }

  this.shadowJavaVM = newJavaVM;
  return newJavaVM;
};

module.exports = JavaVMInterceptor;

},{"../data/java_vm.json":1,"../utils/types":14}],6:[function(require,module,exports){
var JNI_ENV_METHODS = require("../data/jni_env.json");

var Types = require("../utils/types");

var JavaMethod = require("../utils/java_method");

function JNIEnvInterceptor(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
}

JNIEnvInterceptor.prototype.shadowJNIEnv = null;
JNIEnvInterceptor.prototype.methods = {};
JNIEnvInterceptor.prototype.fastMethodLookup = {};

JNIEnvInterceptor.prototype.isInitialised = function () {
  return this.shadowJNIEnv !== null;
};

JNIEnvInterceptor.prototype.get = function () {
  return this.shadowJNIEnv;
};

JNIEnvInterceptor.prototype.createJNIIntercept = function (id, methodAddr) {
  var self = this;
  var method = JNI_ENV_METHODS[id];
  var fridaArgs = [];

  for (var j = 0; j < method.args.length; j++) {
    var ftype = Types.convertNativeJTypeToFridaType(method.args[j]);

    if (ftype !== "va_list") {
      fridaArgs.push(ftype);
    }
  }

  var fridaRet = Types.convertNativeJTypeToFridaType(method.ret);
  var nativeFunction = new NativeFunction(methodAddr, fridaRet, fridaArgs);
  var nativeCallback = new NativeCallback(function () {
    var threadId = this.threadId;
    var localArgs = [].slice.call(arguments);
    var jniEnv = self.threads.getJNIEnv(threadId);
    localArgs[0] = jniEnv;
    var ret = nativeFunction.apply(null, localArgs);
    self.transport.trace(method, localArgs, ret, this.context);

    if (method.name === "GetMethodID" || method.name === "GetStaticMethodID") {
      var signature = Memory.readCString(localArgs[3]);
      var types = new JavaMethod(signature);
      var fridaTypes = {
        params: [],
        javaParams: [],
        ret: NULL
      };

      for (var i = 0; i < types.params.length; i++) {
        var nativeJType = Types.convertJTypeToNativeJType(types.params[i]);
        var fridaType = Types.convertNativeJTypeToFridaType(nativeJType);
        fridaTypes.params.push(fridaType);
        fridaTypes.javaParams.push(Types.convertJTypeToNativeJType(types.params[i]));
      }

      var jTypeRet = Types.convertJTypeToNativeJType(types.ret);
      fridaTypes.ret = Types.convertNativeJTypeToFridaType(jTypeRet);
      self.methods[ret] = fridaTypes;
    } else if (method.name === "RegisterNatives") {
      var methods = localArgs[2];
      var size = localArgs[3];

      for (var i = 0; i < size * 3; i += 3) {
        var offset = (i + 2) * Process.pointerSize;
        var addr = Memory.readPointer(methods.add(offset));
        Interceptor.attach(addr, {
          onEnter: function (args) {
            if (!self.threads.hasJNIEnv(this.threadId)) {
              self.threads.setJNIEnv(this.threadId, ptr(args[0]));
            }

            args[0] = ptr(self.shadowJNIEnv);
          }
        });
      }
    }

    return ret;
  }, fridaRet, fridaArgs);
  this.references.add(nativeCallback);
  return nativeCallback;
};

JNIEnvInterceptor.prototype.createJNIVarArgIntercept = function (id, methodAddr) {
  var self = this;
  var method = JNI_ENV_METHODS[id];
  var text = Memory.alloc(Process.pageSize);
  var data = Memory.alloc(Process.pageSize);
  var vaArgsCallback = NULL;
  var mainCallback = NULL;
  this.references.add(text);
  this.references.add(data);
  vaArgsCallback = new NativeCallback(function () {
    var callbackParams = [];
    var originalParams = [];
    var methodId = arguments[2];
    var vaArgs = self.methods[methodId];

    if (self.fastMethodLookup[methodId]) {
      return self.fastMethodLookup[methodId];
    }

    for (var i = 0; i < method.args.length - 1; i++) {
      var fridaType = Types.convertNativeJTypeToFridaType(method.args[i]);
      callbackParams.push(fridaType);
      originalParams.push(fridaType);
    }

    originalParams.push("...");

    for (var i = 0; i < vaArgs.params.length; i++) {
      if (vaArgs.params[i] === "float") {
        callbackParams.push("double");
      } else {
        callbackParams.push(vaArgs.params[i]);
      }

      originalParams.push(vaArgs.params[i]);
    }

    var retType = Types.convertNativeJTypeToFridaType(method.ret);
    mainCallback = new NativeCallback(function () {
      var threadId = this.threadId;
      var localArgs = [].slice.call(arguments);
      var jniEnv = self.threads.getJNIEnv(threadId);
      localArgs[0] = jniEnv;
      var ret = new NativeFunction(methodAddr, retType, originalParams).apply(null, localArgs);
      self.transport.trace(method, localArgs, ret, this.context, vaArgs.javaParams);
      return ret;
    }, retType, callbackParams);
    self.references.add(mainCallback);
    self.fastMethodLookup[methodId] = mainCallback;
    return mainCallback;
  }, "pointer", ["pointer", "pointer", "pointer"]);
  this.references.add(vaArgsCallback);
  self.buildVaArgParserShellcode(text, data, vaArgsCallback);
  return text;
};

JNIEnvInterceptor.prototype.processVaListRetVal = function (retType, retval, registers) {
  return retval;
};

JNIEnvInterceptor.prototype.createJNIVaListIntercept = function (id, methodAddr) {
  var self = this;
  var methodData = JNI_ENV_METHODS[id];
  var retType = Types.convertNativeJTypeToFridaType(methodData.ret);
  Interceptor.attach(methodAddr, {
    onEnter: function (args) {
      var threadId = this.threadId;
      this.shadowJNIEnv = self.threads.getJNIEnv(threadId);
      this.localJNIEnv = ptr(args[0]);

      if (!this.shadowJNIEnv.isNull() && !this.localJNIEnv.equals(this.shadowJNIEnv)) {
        this.methodId = ptr(args[2]);
        var vaList = ptr(args[3]);
        this.args = [this.localJNIEnv, args[1], this.methodId];
        this.ret = NULL;
        var method = self.methods[this.methodId];

        if (!method) {
          return;
        }

        self.setUpVaListArgExtract(vaList);

        for (var i = 0; i < method.params.length; i++) {
          var val = NULL;
          var currentPtr = self.extractVaListArgValue(method, i);

          if (method.params[i] === "char") {
            val = Memory.readS8(currentPtr);
          } else if (method.params[i] === "int16") {
            val = Memory.readS16(currentPtr);
          } else if (method.params[i] === "uint16") {
            val = Memory.readU16(currentPtr);
          } else if (method.params[i] === "int") {
            val = Memory.readS32(currentPtr);
          } else if (method.params[i] === "int64") {
            val = Memory.readS64(currentPtr);
          } else if (method.params[i] === "float") {
            val = Memory.readDouble(currentPtr);
          } else if (method.params[i] === "double") {
            val = Memory.readDouble(currentPtr);
          } //TODO - needs to use jtype


          this.args.push(val);
        }

        self.resetVaListArgExtract();
        args[0] = this.shadowJNIEnv;
      }
    },
    onLeave: function (originalRet) {
      if (!this.shadowJNIEnv.isNull() && !this.localJNIEnv.equals(this.shadowJNIEnv)) {
        var ret = NULL;
        var retval = self.processVaListRetVal(retType, ptr(originalRet), this.context);

        if (retType === "int8") {
          ret = retval.toInt32();
        } else if (retType === "int16") {
          ret = retval.toInt32();
        } else if (retType === "uint16") {
          ret = retval.toInt32();
        } else if (retType === "int32") {
          ret = retval.toInt32();
        } else if (retType === "int64") {
          ret = uint64("0x" + retval.toString());
        } else if (retType === "float") {
          var buf = Memory.alloc(Types.sizeOf(retType));
          Memory.writeS32(buf, retval.toInt32());
          ret = Memory.readFloat(buf);
        } else if (retType === "double") {
          var buf = Memory.alloc(Types.sizeOf(retType));
          Memory.writeU64(buf, uint64("0x" + retval.toString()));
          ret = Memory.readDouble(buf);
        }

        var add = self.methods[this.methodId].javaParams;
        self.transport.trace(methodData, this.args, ret, this.context, add);
      }
    }
  });
  return methodAddr;
};

JNIEnvInterceptor.prototype.create = function () {
  var threadId = Process.getCurrentThreadId();
  var jniEnv = this.threads.getJNIEnv(threadId);
  var jniEnvOffset = 4;
  var jniEnvLength = 232;
  var newJNIEnvStruct = Memory.alloc(Process.pointerSize * jniEnvLength);
  this.references.add(newJNIEnvStruct);
  var newJNIEnv = Memory.alloc(Process.pointerSize);
  Memory.writePointer(newJNIEnv, newJNIEnvStruct);
  this.references.add(newJNIEnv);

  for (var i = jniEnvOffset; i < jniEnvLength; i++) {
    var method = JNI_ENV_METHODS[i];
    var offset = i * Process.pointerSize;
    var jniEnvStruct = Memory.readPointer(jniEnv);
    var methodAddr = Memory.readPointer(jniEnvStruct.add(offset));

    if (method.args[method.args.length - 1] === "...") {
      var callback = this.createJNIVarArgIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    } else if (method.args[method.args.length - 1] === "va_list") {
      var callback = this.createJNIVaListIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    } else {
      var callback = this.createJNIIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    }
  }

  this.shadowJNIEnv = newJNIEnv;
  return newJNIEnv;
};

module.exports = JNIEnvInterceptor;

},{"../data/jni_env.json":2,"../utils/java_method":12,"../utils/types":14}],7:[function(require,module,exports){
function JNIThreadManager() {
  this.threads = {};
  this.shadowJavaVM = NULL;
}

JNIThreadManager.prototype.createEntry = function (threadId) {
  if (!this.threads[threadId]) {
    this.threads[threadId] = {
      'jniEnv': NULL
    };
  }

  return this.threads[threadId];
};

JNIThreadManager.prototype.getJavaVM = function () {
  return this.shadowJavaVM;
};

JNIThreadManager.prototype.hasJavaVM = function () {
  return !this.shadowJavaVM.isNull();
};

JNIThreadManager.prototype.setJavaVM = function (javaVM) {
  this.shadowJavaVM = javaVM;
};

JNIThreadManager.prototype.getJNIEnv = function (threadId) {
  var entry = this.createEntry(threadId);
  return entry.jniEnv;
};

JNIThreadManager.prototype.hasJNIEnv = function (threadId) {
  return !this.getJNIEnv(threadId).isNull();
};

JNIThreadManager.prototype.setJNIEnv = function (threadId, jniEnv) {
  var entry = this.createEntry(threadId);
  entry.jniEnv = jniEnv;
};

JNIThreadManager.prototype.needsJNIEnvUpdate = function (threadId, jniEnv) {
  var entry = this.createEntry(threadId);

  if (!entry.jniEnv.equals(jniEnv)) {
    return true;
  }

  return false;
};

module.exports = JNIThreadManager;

},{}],8:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

function JNIEnvInterceptorX64(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.grOffset = NULL;
  this.grOffsetStart = NULL;
  this.fpOffset = NULL;
  this.fpOffsetStart = NULL;
  this.overflowPtr = NULL;
  this.dataPtr = NULL;
}

JNIEnvInterceptorX64.prototype = new JNIEnvInterceptor();

JNIEnvInterceptor.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new X86Writer(code, {
      pc: text
    });
    var dataOffset = 0;
    var xmmOffset = 0;
    var regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9", "rax", "rbx", "r10", "r11", "r12", "r13", "r14", "r15", "xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7"];

    for (var i = 0; i < regs.length; i++) {
      cw.putMovNearPtrReg(data.add(dataOffset), "rdi");
      dataOffset += Process.pointerSize;

      if (i < regs.length - 1) {
        if (regs[i + 1].indexOf("xmm") > -1) {
          cw.putU8(0x66);
          cw.putU8(0x48);
          cw.putU8(0x0f);
          cw.putU8(0x7e);
          cw.putU8(0xc7 + xmmOffset * 8);
          xmmOffset++;
        } else {
          cw.putMovRegReg("rdi", regs[i + 1]);
        }
      }
    }

    xmmOffset--;
    cw.putPopReg("rdi");
    cw.putMovNearPtrReg(data.add(dataOffset), "rdi");
    dataOffset += Process.pointerSize;
    cw.putCallAddress(parser);
    cw.putMovNearPtrReg(data.add(dataOffset), "rax");
    dataOffset += Process.pointerSize;
    var regRestoreOffset = dataOffset - Process.pointerSize * 2;

    for (var i = regs.length - 1; i >= 0; i--) {
      var regRestoreOffset = i * Process.pointerSize;
      cw.putMovRegNearPtr("rdi", data.add(regRestoreOffset));

      if (i > 0) {
        if (regs[i].indexOf("xmm") > -1) {
          cw.putU8(0x66);
          cw.putU8(0x48);
          cw.putU8(0x0f);
          cw.putU8(0x6e);
          cw.putU8(0xc7 + xmmOffset * 8);
          xmmOffset--;
        } else {
          cw.putMovRegReg(regs[i], "rdi");
        }
      }
    }

    cw.putMovNearPtrReg(data.add(dataOffset), "rdi");
    var rdiBackup = dataOffset;
    dataOffset += Process.pointerSize;
    var cbAddressOffset = rdiBackup - Process.pointerSize;
    cw.putMovRegNearPtr("rdi", data.add(cbAddressOffset));
    cw.putMovNearPtrReg(data.add(dataOffset), "r13");
    var r13Backup = dataOffset;
    cw.putMovRegReg("r13", "rdi");
    cw.putMovRegNearPtr("rdi", data.add(rdiBackup));
    cw.putCallReg("r13");
    cw.putMovRegNearPtr("r13", data.add(r13Backup));
    var retAddressOffset = cbAddressOffset - Process.pointerSize;
    cw.putJmpNearPtr(data.add(retAddressOffset));
    cw.flush();
  });
};

JNIEnvInterceptorX64.prototype.setUpVaListArgExtract = function (vaList) {
  this.grOffset = Memory.readU32(vaList);
  this.grOffsetStart = this.grOffset;
  this.fpOffset = Memory.readU32(vaList.add(4));
  this.fpOffsetStart = this.fpOffset;
  this.overflowPtr = Memory.readPointer(vaList.add(Process.pointerSize));
  this.dataPtr = Memory.readPointer(vaList.add(Process.pointerSize * 2));
};

JNIEnvInterceptorX64.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = NULL;

  if (method.params[paramId] === "float" || method.params[paramId] === "double") {
    if ((this.fpOffset - this.fpOffsetStart) / Process.pointerSize < 14) {
      currentPtr = this.dataPtr.add(this.fpOffset);
      this.fpOffset += Process.pointerSize * 2;
    } else {
      var reverseId = method.params.length - paramId - 1;
      currentPtr = this.overflowPtr.add(reverseId * Process.pointerSize);
    }
  } else {
    if ((this.grOffset - this.grOffsetStart) / Process.pointerSize < 2) {
      currentPtr = this.dataPtr.add(this.grOffset);
      this.grOffset += Process.pointerSize;
    } else {
      var reverseId = method.params.length - paramId - 1;
      currentPtr = this.overflowPtr.add(reverseId * Process.pointerSize);
    }
  }

  return currentPtr;
};

JNIEnvInterceptorX64.prototype.resetVaListArgExtract = function () {
  this.grOffset = NULL;
  this.grOffsetStart = NULL;
  this.fpOffset = NULL;
  this.fpOffsetStart = NULL;
  this.overflowPtr = NULL;
  this.dataPtr = NULL;
};

module.exports = JNIEnvInterceptorX64;

},{"../jni_env_interceptor":6}],9:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

var Types = require("../../utils/types");

function JNIEnvInterceptorX86(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.vaList = NULL;
  this.vaListOffset = 0;
}

JNIEnvInterceptorX86.prototype = new JNIEnvInterceptor();

JNIEnvInterceptorX86.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  Memory.writePointer(text.add(0x400), parser);
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new X86Writer(code, {
      pc: text
    });
    var dataOffset = 0x400 + Process.pointerSize;
    cw.putPopReg("eax");
    cw.putMovNearPtrReg(text.add(dataOffset + Process.pointerSize), "eax");
    cw.putCallAddress(parser);
    cw.putCallReg("eax");
    cw.putJmpNearPtr(text.add(dataOffset + Process.pointerSize));
    cw.flush();
  }); // required for some reason...

  Interceptor.attach(text.add(0), function () {});
};

JNIEnvInterceptorX86.prototype.setUpVaListArgExtract = function (vaList) {
  this.vaList = vaList;
  this.vaListOffset = 0;
};

JNIEnvInterceptorX86.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = this.vaList.add(this.vaListOffset);
  this.vaListOffset += Types.sizeOf(method.params[paramId]);
  return currentPtr;
};

JNIEnvInterceptorX86.prototype.resetVaListArgExtract = function () {
  this.vaList = NULL;
  this.vaListOffset = 0;
};

JNIEnvInterceptorX86.prototype.processVaListRetVal = function (retType, retval, registers) {
  if (retType === "int64") {
    retval = registers.edx.toString().substring(2) + registers.eax.toString().substring(2);
  } else if (retType === "double" || retType === "float") {//TODO - currently does not support floating point returns on x86
  }

  return retval;
};

module.exports = JNIEnvInterceptorX86;

},{"../../utils/types":14,"../jni_env_interceptor":6}],10:[function(require,module,exports){
var Types = require("./utils/types");

var JavaMethod = require("./utils/java_method");

var JNIThreadManager = require("./jni/jni_thread_manager");

var ReferenceManager = require("./utils/reference_manager");

var TraceTransport = require("./transport/trace_transport");

var JNIEnvInterceptorX86 = require("./jni/x86/jni_env_interceptor_x86");

var JNIEnvInterceptorX64 = require("./jni/x64/jni_env_interceptor_x64");

var JNIEnvInterceptorARM = require("./jni/arm/jni_env_interceptor_arm");

var JNIEnvInterceptorARM64 = require("./jni/arm64/jni_env_interceptor_arm64");

var JavaVMInterceptor = require("./jni/java_vm_interceptor");

var threads = new JNIThreadManager();
var references = new ReferenceManager();
var transport = new TraceTransport(threads);
var jniEnvInterceptor = null;

if (Process.arch === "ia32") {
  jniEnvInterceptor = new JNIEnvInterceptorX86(references, threads, transport);
} else if (Process.arch === "x64") {
  jniEnvInterceptor = new JNIEnvInterceptorX64(references, threads, transport);
} else if (Process.arch === "arm") {
  jniEnvInterceptor = new JNIEnvInterceptorARM(references, threads, transport);
} else if (Process.arch === "arm64") {
  jniEnvInterceptor = new JNIEnvInterceptorARM64(references, threads, transport);
}

if (!jniEnvInterceptor) {
  throw new Error(Process.arch + " currently unsupported, please file an issue.");
}

var javaVMInterceptor = new JavaVMInterceptor(references, threads, jniEnvInterceptor);
var libsToTrack = ['*'];
var trackedLibs = {};
var libBlacklist = {}; // need to run this before start up.

function checkLibrary(path) {
  if (libsToTrack.length === 0) {
    var op = recv('libraries', function (message) {
      libsToTrack = message.payload;
    });
    op.wait();
  }

  if (libsToTrack.length === 1) {
    if (libsToTrack[0] === "*") {
      return true;
    }
  }

  for (var i = 0; i < libsToTrack.length; i++) {
    if (path.indexOf(libsToTrack[i]) > -1) {
      return true;
    }
  }

  return false;
}

function interceptJNIOnLoad(jniOnLoadAddr) {
  return Interceptor.attach(jniOnLoadAddr, {
    onEnter: function (args) {
      var shadowJavaVM = NULL;
      var javaVM = ptr(args[0]);

      if (!threads.hasJavaVM()) {
        threads.setJavaVM(javaVM);
      }

      if (!javaVMInterceptor.isInitialised()) {
        shadowJavaVM = javaVMInterceptor.create();
      } else {
        shadowJavaVM = javaVMInterceptor.get();
      }

      args[0] = shadowJavaVM;
    }
  });
}

function interceptJNIFunction(jniFunctionAddr) {
  return Interceptor.attach(jniFunctionAddr, {
    onEnter: function (args) {
      var shadowJNIEnv = NULL;
      var threadId = this.threadId;
      var jniEnv = ptr(args[0]);
      threads.setJNIEnv(threadId, jniEnv);

      if (!jniEnvInterceptor.isInitialised()) {
        shadowJNIEnv = jniEnvInterceptor.create();
      } else {
        shadowJNIEnv = jniEnvInterceptor.get();
      }

      args[0] = shadowJNIEnv;
    }
  });
}

var dlopenRef = Module.findExportByName(null, "dlopen");
var dlsymRef = Module.findExportByName(null, "dlsym");
var dlcloseRef = Module.findExportByName(null, "dlclose");

if (dlopenRef && dlsymRef && dlcloseRef) {
  var dlopen = new NativeFunction(dlopenRef, 'pointer', ['pointer', 'int']);
  Interceptor.replace(dlopen, new NativeCallback(function (filename, mode) {
    var path = Memory.readCString(filename);
    var retval = dlopen(filename, mode);

    if (checkLibrary(path)) {
      trackedLibs[ptr(retval)] = true;
    } else {
      libBlacklist[ptr(retval)] = true;
    }

    return retval;
  }, 'pointer', ['pointer', 'int']));
  var dlsym = new NativeFunction(dlsymRef, "pointer", ["pointer", "pointer"]);
  Interceptor.attach(dlsym, {
    onEnter: function (args) {
      this.handle = ptr(args[0]);

      if (libBlacklist[this.handle]) {
        return;
      }

      this.symbolAddr = ptr(args[1]);
    },
    onLeave: function (retval) {
      if (retval.isNull() || libBlacklist[this.handle]) {
        return;
      }

      if (!trackedLibs[this.handle]) {
        // Android 7 and above miss the initial dlopen call.
        // Give it another chance in dlsym.
        var mod = Process.findModuleByAddress(retval);

        if (checkLibrary(mod.name)) {
          trackedLibs[this.handle] = true;
        }
      }

      if (trackedLibs[this.handle]) {
        var symbol = Memory.readCString(this.symbolAddr);

        if (symbol === "JNI_OnLoad") {
          interceptJNIOnLoad(ptr(retval));
        } else if (symbol.startsWith("Java_")) {
          interceptJNIFunction(ptr(retval));
        }
      } else {
        var name = libsToTrack[0];

        if (name !== "*") {
          var mod = Process.findModuleByAddress(retval);
          name = mod.name;
        }

        if (libsToTrack.indexOf(name) > -1 || name === "*") {
          interceptJNIFunction(ptr(retval));
        }
      }
    }
  });
  var dlclose = new NativeFunction(dlcloseRef, "int", ["pointer"]);
  Interceptor.attach(dlclose, {
    onEnter: function (args) {
      var handle = ptr(args[0]);

      if (trackedLibs[handle]) {
        this.handle = handle;
      }
    },
    onLeave: function (retval) {
      if (this.handle) {
        if (retval.isNull()) {
          delete trackedLibs[this.handle];
        }
      }
    }
  });
}

if (libsToTrack.length > 0) {
  console.error("Welcome to jnitrace. Tracing is running...");
  console.warn("NOTE: the recommended way to run this module is using the " + "python wrapper. It provides nicely formated coloured output " + "in the form of frida-trace. To get jnitrace run " + "'pip install jnitrace' or go to " + "'https://github.com/chame1eon/jnitrace'");
}

},{"./jni/arm/jni_env_interceptor_arm":4,"./jni/arm64/jni_env_interceptor_arm64":3,"./jni/java_vm_interceptor":5,"./jni/jni_thread_manager":7,"./jni/x64/jni_env_interceptor_x64":8,"./jni/x86/jni_env_interceptor_x86":9,"./transport/trace_transport":11,"./utils/java_method":12,"./utils/reference_manager":13,"./utils/types":14}],11:[function(require,module,exports){
var Types = require("../utils/types");

function TraceTransport(threads) {
  this.threads = threads;
  this.start = Date.now();
} // add - additional method data - will include jtypes for va_list and ...


TraceTransport.prototype.trace = function (method, args, ret, context, add) {
  var threadId = Process.getCurrentThreadId();
  var outputArgs = [];
  var outputRet = NULL;
  var jniEnv = this.threads.getJNIEnv(threadId);
  var sendData = null;
  outputArgs.push({
    value: jniEnv
  });

  if (method.name === "DefineClass") {
    var name = Memory.readCString(args[1]);
    args.push({
      value: args[1],
      data: name
    });
    args.push({
      value: args[2]
    });
    var classData = Memory.readByteArray(args[3], args[4]);
    args.push({
      value: args[3],
      data_for: 3
    });
    sendData = classData;
    args.push({
      value: args[4]
    });
  } else if (method.name === "FindClass") {
    var name = Memory.readCString(args[1]);
    outputArgs.push({
      value: args[1],
      data: name
    });
  } else if (method.name === "ThrowNew") {
    var message = Memory.readCString(args[2]);
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: message
    });
  } else if (method.name === "FatalError") {
    var message = Memory.readCString(args[1]);
    outputArgs.push({
      value: args[1],
      data: message
    });
  } else if (method.name.endsWith("ID")) {
    var name = Memory.readCString(args[2]);
    var sig = Memory.readCString(args[3]);
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: name
    });
    outputArgs.push({
      value: args[3],
      data: sig
    });
  } else if (method.name === "NewString") {
    var unicode = Memory.readByteArray(args[1], args[2]);
    outputArgs.push({
      value: args[1],
      data_for: 1
    });
    sendData = unicode;
    outputArgs.push({
      value: args[2]
    });
  } else if (method.name.startsWith("Get") && method.name.endsWith("Chars") || method.name.endsWith("Elements") || method.name.endsWith("ArrayCritical") || method.name === "GetStringCritical") {
    outputArgs.push({
      value: args[1]
    });

    if (!args[2].isNull()) {
      outputArgs.push({
        value: args[2],
        data: Memory.readU32(args[2])
      });
    } else {
      outputArgs.push({
        value: args[2]
      });
    }

    if (args.length > 3) {
      outputArgs.push({
        value: args[3]
      });
    }
  } else if (method.name.startsWith("Release") && method.name.endsWith("Chars")) {
    var unicode = Memory.readCString(args[2]);
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: unicode
    });
  } else if (method.name.endsWith("Region")) {
    var type = method.args[4].substring(0, method.args[4].length - 1);
    var nType = Types.convertNativeJTypeToFridaType(type);
    var size = Types.sizeOf(nType);
    var region = Memory.readByteArray(args[4], args[3] * size);

    for (var i = 1; i < args.length - 1; i++) {
      outputArgs.push({
        value: args[i]
      });
    }

    outputArgs.push({
      value: args[args.length - 1],
      data_for: args.length - 1
    });
    sendData = region;
  } else if (method.name === "NewStringUTF") {
    var utf = Memory.readUtf8String(args[1]);
    outputArgs.push({
      value: args[1],
      data: utf
    });
  } else if (method.name === "RegisterNatives") {
    outputArgs.push({
      value: args[1]
    });
    var size = args[3];
    var data = [];

    for (var i = 0; i < size * 3; i += 3) {
      var namePtr = Memory.readPointer(args[2].add(i * Process.pointerSize));
      var name = Memory.readCString(namePtr);
      var sigPtr = Memory.readPointer(args[2].add((i + 1) * Process.pointerSize));
      var sig = Memory.readCString(sigPtr);
      var addr = Memory.readPointer(args[2].add((i + 2) * Process.pointerSize));
      data.push({
        name: {
          value: namePtr,
          data: name
        },
        sig: {
          value: sigPtr,
          data: sig
        },
        addr: {
          value: addr
        }
      });
    }

    outputArgs.push({
      value: args[2],
      data: data
    });
    outputArgs.push({
      value: args[3]
    });
  } else if (method.name === "GetJavaVM") {
    outputArgs.push({
      value: args[1],
      data: Memory.readPointer(args[1])
    });
  } else if (method.name === "ReleaseStringCritical") {
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: Memory.readCString(args[2])
    });
  } else {
    for (var i = 1; i < args.length; i++) {
      outputArgs.push({
        value: args[i]
      });
    }
  }

  outputRet = ret;
  var backtrace = []; // verify that a backtrace is possible.
  // sometimes the NativeCallback provides erroneous CpuContexts

  if (Process.findModuleByAddress(context.pc) && Process.findModuleByAddress(context.sp)) {
    var bt = Thread.backtrace(context, Backtracer.FUZZY);

    for (var i = 0; i < bt.length; i++) {
      backtrace.push({
        address: bt[i],
        module: Process.findModuleByAddress(bt[i])
      });
    }
  }

  send({
    method: method,
    args: outputArgs,
    ret: outputRet,
    threadId: Process.getCurrentThreadId(),
    backtrace: backtrace,
    timestamp: Date.now() - this.start,
    additional_params: add
  }, sendData);
};

module.exports = TraceTransport;

},{"../utils/types":14}],12:[function(require,module,exports){
function JavaMethod(signature) {
  var primitiveTypes = ["B", "S", "I", "J", "F", "D", "C", "Z", "V"];
  var isArray = false;
  var isRet = false;
  var jParamTypes = [];
  var jRetType = null;

  for (var i = 0; i < signature.length; i++) {
    if (signature.charAt(i) === "(") {
      continue;
    }

    if (signature.charAt(i) === ")") {
      isRet = true;
      continue;
    }

    if (signature.charAt(i) === "[") {
      isArray = true;
      continue;
    }

    var jtype = null;

    if (primitiveTypes.indexOf(signature.charAt(i)) > -1) {
      jtype = signature.charAt(i);
    } else if (signature.charAt(i) === "L") {
      var end = signature.indexOf(";", i) + 1;
      jtype = signature.substring(i, end);
      i = end - 1;
    } //TODO DELETE


    if (isArray) {
      jtype = "[" + jtype;
    }

    if (!isRet) {
      jParamTypes.push(jtype);
    } else {
      jRetType = jtype;
    }

    isArray = false;
  }

  this.signature = signature;
  this.params = jParamTypes;
  this.ret = jRetType;
}

JavaMethod.prototype.getParams = function () {
  return this.params;
};

JavaMethod.prototype.getRet = function () {
  return this.ret;
};

module.exports = JavaMethod;

},{}],13:[function(require,module,exports){
function ReferenceManager() {
  this.references = {};
}

ReferenceManager.prototype.add = function (ref) {
  this.references[ref] = ref;
};

ReferenceManager.prototype.release = function (ref) {
  if (this.references[ref]) {
    delete this.references[ref];
  }
};

module.exports = ReferenceManager;

},{}],14:[function(require,module,exports){
function Types() {}

Types.sizeOf = function (type) {
  if (type === "double" || type === "float" || type === "int64") {
    return 8;
  } else if (type === "char") {
    return 1;
  } else {
    return Process.pointerSize;
  }
};

Types.convertNativeJTypeToFridaType = function (jtype) {
  if (jtype.indexOf("*") > -1) {
    return "pointer";
  }

  if (jtype === "jmethodID") {
    return "pointer";
  }

  if (jtype === "jfieldID") {
    return "pointer";
  }

  if (jtype === "va_list") {
    return "va_list";
  }

  if (jtype === "jweak") {
    jtype = "jobject";
  }

  if (jtype === "jthrowable") {
    jtype = "jobject";
  }

  if (jtype.indexOf("Array") > -1) {
    jtype = "jarray";
  }

  if (jtype === "jarray") {
    jtype = "jobject";
  }

  if (jtype === "jstring") {
    jtype = "jobject";
  }

  if (jtype === "jclass") {
    jtype = "jobject";
  }

  if (jtype === "jobject") {
    return "pointer";
  }

  if (jtype === "jsize") {
    jtype = "jint";
  }

  if (jtype === "jdouble") {
    return "double";
  }

  if (jtype === "jfloat") {
    return "float";
  }

  if (jtype === "jchar") {
    return "uint16";
  }

  if (jtype === "jboolean") {
    return "char";
  }

  if (jtype === "jlong") {
    return "int64";
  }

  if (jtype === "jint") {
    return "int";
  }

  if (jtype === "jshort") {
    return "int16";
  }

  if (jtype === "jbyte") {
    return "char";
  }

  return jtype;
};

Types.convertJTypeToNativeJType = function (jtype, isArray) {
  var primitiveTypes = ["B", "S", "I", "J", "F", "D", "C", "Z"];
  var result = "";

  if (jtype === "B") {
    result += "jbyte";
  } else if (jtype === "S") {
    result += "jshort";
  } else if (jtype === "I") {
    result += "jint";
  } else if (jtype === "J") {
    result += "jlong";
  } else if (jtype === "F") {
    result += "jfloat";
  } else if (jtype === "D") {
    result += "jdouble";
  } else if (jtype === "C") {
    result += "jchar";
  } else if (jtype === "Z") {
    result += "jboolean";
  } else if (jtype.charAt(0) === "L") {
    if (jtype === "Ljava/lang/String;") {
      result += "jstring";
    } else if (jtype === "Ljava/lang/Class;") {
      result += "jclass";
    } else {
      result += "jobject";
    }
  }

  if (isArray) {
    if (result === "jstring") {
      result = "jobject";
    }

    result += "Array";
  }

  return result;
};

module.exports = Types;

},{}]},{},[10])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL0FwcERhdGEvUm9hbWluZy9ucG0vbm9kZV9tb2R1bGVzL2ZyaWRhLWNvbXBpbGUvbm9kZV9tb2R1bGVzL2Jyb3dzZXItcGFjay9fcHJlbHVkZS5qcyIsImRhdGEvamF2YV92bS5qc29uIiwiZGF0YS9qbmlfZW52Lmpzb24iLCJqbmkvYXJtNjQvam5pX2Vudl9pbnRlcmNlcHRvcl9hcm02NC5qcyIsImpuaS9hcm0vam5pX2Vudl9pbnRlcmNlcHRvcl9hcm0uanMiLCJqbmkvamF2YV92bV9pbnRlcmNlcHRvci5qcyIsImpuaS9qbmlfZW52X2ludGVyY2VwdG9yLmpzIiwiam5pL2puaV90aHJlYWRfbWFuYWdlci5qcyIsImpuaS94NjQvam5pX2Vudl9pbnRlcmNlcHRvcl94NjQuanMiLCJqbmkveDg2L2puaV9lbnZfaW50ZXJjZXB0b3JfeDg2LmpzIiwibWFpbi5qcyIsInRyYW5zcG9ydC90cmFjZV90cmFuc3BvcnQuanMiLCJ1dGlscy9qYXZhX21ldGhvZC5qcyIsInV0aWxzL3JlZmVyZW5jZV9tYW5hZ2VyLmpzIiwidXRpbHMvdHlwZXMuanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7QUNBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQzFEQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFD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LE1BQUksS0FBSyxLQUFLLFFBQWQsRUFBd0I7QUFDdEIsV0FBTyxPQUFQO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssT0FBZCxFQUF1QjtBQUNyQixXQUFPLE1BQVA7QUFDRDs7QUFFRCxTQUFPLEtBQVA7QUFDRCxDQS9ERDs7QUFpRUEsS0FBSyxDQUFDLHlCQUFOLEdBQWtDLFVBQVMsS0FBVCxFQUFnQixPQUFoQixFQUF5QjtBQUN6RCxNQUFJLGNBQWMsR0FBRyxDQUFDLEdBQUQsRUFBTSxHQUFOLEVBQVcsR0FBWCxFQUFnQixHQUFoQixFQUFxQixHQUFyQixFQUEwQixHQUExQixFQUErQixHQUEvQixFQUFvQyxHQUFwQyxDQUFyQjtBQUNBLE1BQUksTUFBTSxHQUFHLEVBQWI7O0FBRUEsTUFBSSxLQUFLLEtBQUssR0FBZCxFQUFtQjtBQUNqQixJQUFBLE1BQU0sSUFBSSxPQUFWO0FBQ0QsR0FGRCxNQUVPLElBQUksS0FBSyxLQUFLLEdBQWQsRUFBbUI7QUFDeEIsSUFBQSxNQUFNLElBQUksUUFBVjtBQUNELEdBRk0sTUFFQSxJQUFJLEtBQUssS0FBSyxHQUFkLEVBQW1CO0FBQ3hCLElBQUEsTUFBTSxJQUFJLE1BQVY7QUFDRCxHQUZNLE1BRUEsSUFBSSxLQUFLLEtBQUssR0FBZCxFQUFtQjtBQUN4QixJQUFBLE1BQU0sSUFBSSxPQUFWO0FBQ0QsR0FGTSxNQUVBLElBQUksS0FBSyxLQUFLLEdBQWQsRUFBbUI7QUFDeEIsSUFBQSxNQUFNLElBQUksUUFBVjtBQUNELEdBRk0sTUFFQSxJQUFJLEtBQUssS0FBSyxHQUFkLEVBQW1CO0FBQ3hCLElBQUEsTUFBTSxJQUFJLFNBQVY7QUFDRCxHQUZNLE1BRUEsSUFBSSxLQUFLLEtBQUssR0FBZCxFQUFtQjtBQUN4QixJQUFBLE1BQU0sSUFBSSxPQUFWO0FBQ0QsR0FGTSxNQUVBLElBQUksS0FBSyxLQUFLLEdBQWQsRUFBbUI7QUFDeEIsSUFBQSxNQUFNLElBQUksVUFBVjtBQUNELEdBRk0sTUFFQSxJQUFJLEtBQUssQ0FBQyxNQUFOLENBQWEsQ0FBYixNQUFvQixHQUF4QixFQUE2QjtBQUNsQyxRQUFJLEtBQUssS0FBSyxvQkFBZCxFQUFvQztBQUNsQyxNQUFBLE1BQU0sSUFBSSxTQUFWO0FBQ0QsS0FGRCxNQUVPLElBQUcsS0FBSyxLQUFLLG1CQUFiLEVBQWtDO0FBQ3ZDLE1BQUEsTUFBTSxJQUFJLFFBQVY7QUFDRCxLQUZNLE1BRUE7QUFDTCxNQUFBLE1BQU0sSUFBSSxTQUFWO0FBQ0Q7QUFDRjs7QUFFRCxNQUFJLE9BQUosRUFBYTtBQUNYLFFBQUksTUFBTSxLQUFLLFNBQWYsRUFBMEI7QUFDeEIsTUFBQSxNQUFNLEdBQUcsU0FBVDtBQUNEOztBQUNELElBQUEsTUFBTSxJQUFJLE9BQVY7QUFDRDs7QUFFRCxTQUFPLE1BQVA7QUFDRCxDQXRDRDs7QUF3Q0EsTUFBTSxDQUFDLE9BQVAsR0FBaUIsS0FBakIiLCJmaWxlIjoiZ2VuZXJhdGVkLmpzIiwic291cmNlUm9vdCI6IiJ9
