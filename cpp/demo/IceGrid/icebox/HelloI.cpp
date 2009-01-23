// **********************************************************************
//
// Copyright (c) 2003-2009 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

#include <Ice/Ice.h>
#include <HelloI.h>

using namespace std;

HelloI::HelloI(const string& serviceName) :
    _serviceName(serviceName)
{
}

void
HelloI::sayHello(const Ice::Current&)
{
    cout << "Hello from " << _serviceName << endl;
}
