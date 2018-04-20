// **********************************************************************
//
// Copyright (c) 2003-2018 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

package com.zeroc.Ice;

/**
 * The signal policy for Ice.Application signal handling.
 *
 * @see Application
 **/
public enum SignalPolicy
{
    /**
     * If a signal is received, {@link Application} reacts to the signal
     * by calling {@link Communicator#destroy} or {@link Communicator#shutdown},
     * or by calling a custom shutdown hook installed by the application.
     **/
    HandleSignals,

    /**
     * Any signal that is received is not intercepted and takes the default
     * action.
     **/
    NoSignalHandling
}