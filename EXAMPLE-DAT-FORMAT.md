# Example .dat file format

This is an example of what your .dat file should contain:

```
'guest_account_info":("com.garena.msdk.guest_password":"2B70759365BF3B96CC4415ACD26B407EF713D8D170D37AE682214735D77DCF2F", "com.garena.msdk.guest_uid":"4340622430")
```

The app will automatically extract:
- **UID**: 4340622430
- **Password**: 2B70759365BF3B96CC4415ACD26B407EF713D8D170D37AE682214735D77DCF2F

## Supported formats:

The parser is flexible and will find:
- `com.garena.msdk.guest_uid` followed by digits
- `com.garena.msdk.guest_password` followed by hex characters (A-F, 0-9)

Even if your .dat file has extra data or different formatting, it should work!
