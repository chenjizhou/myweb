# -*- coding: utf-8 -*-

class RET:
    OK                  = "0"
    DBERR               = "4001"
    NODATA              = "4002"
    DATAEXIST           = "4003"
    DATAERR             = "4004"
    SESSIONERR          = "4101"
    LOGINERR            = "4102"
    PARAMERR            = "4103"
    USERERR             = "4104"
    ROLEERR             = "4105"
    PWDERR              = "4106"
    REQERR              = "4201"
    IPERR               = "4202"
    THIRDERR            = "4301"
    IOERR               = "4302"
    SERVERERR           = "4500"
    UNKNOWNERR          = "4501"


error_map = {
    RET.OK                  : "success",
    RET.DBERR               : "database error",
    RET.NODATA              : "not found",
    RET.DATAEXIST           : "data existed",
    RET.DATAERR             : "data error",
    RET.SESSIONERR          : "used not login",
    RET.LOGINERR            : "login error",
    RET.PARAMERR            : "param error",
    RET.USERERR             : "user not existed",
    RET.ROLEERR             : "role error",
    RET.PWDERR              : "password error",
    RET.REQERR              : "invalid request or request limited",
    RET.IPERR               : "IP error",
    RET.THIRDERR            : "three party plugin error",
    RET.IOERR               : "IO error",
    RET.SERVERERR           : "server error",
    RET.UNKNOWNERR          : "unknown error",
}
