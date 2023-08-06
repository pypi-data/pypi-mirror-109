import os ,hashlib ,uuid ,base64 
from datetime import date ,datetime 
class craxk_128 ():
    digest_size =''
    block_size =''
    def __init__ (O0O0OO0O0O000O00O ,O0OO0O0OOOOOO0O00 =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (O0OO0O0OOOOOO0O00 ,(str ,int ,float ))!=True :
            O0O0OO0O0O000O00O .data =O0OO0O0OOOOOO0O00 
        else :
            O0O0OO0O0O000O00O .data =bytes (str (O0OO0O0OOOOOO0O00 ),'utf-8')
        OOO00O00000O000OO =uuid .getnode ()
        O0OO00OOOO00OO0O0 =base64 .encodebytes (bytes (str (OOO00O00000O000OO ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0O0OO0O0O000O00O .data +O0OO00OOOO00OO0O0 )
            hash128_2 =hashlib .shake_256 (O0O0OO0O0O000O00O .data +O0OO00OOOO00OO0O0 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O0O0OO0O0O000O00O .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (O0OO00OOOO00OO0O0 ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        O0OOO0OO00O0OO0OO =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        O0OOO00OO0O0OOOOO =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        OOO0OO00OOOO00O00 =O0OOO0OO00O0OO0OO +UUIDHASH128_3 .digest ()
        OO00OO0000O0O00OO =O0OOO00OO0O0OOOOO +UUIDHASH128_3 .hexdigest ()
        craxk_128 .digest_size =len (OOO0OO00OOOO00O00 )
        craxk_128 .block_size =len (OO00OO0000O0O00OO )
    def update (OO0OO000O00OOO0O0 ,OOO0OO00O0OO0OO0O =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OOO0OO00O0OO0OO0O ,(str ,int ,float ))!=True :
            OO0OO000O00OOO0O0 .data =OO0OO000O00OOO0O0 .data +OOO0OO00O0OO0OO0O 
        else :
            OO0OO000O00OOO0O0 .data =OO0OO000O00OOO0O0 .data +bytes (str (OOO0OO00O0OO0OO0O ),'utf-8')
        OOO0OOO0O0O0O000O =date .today ()
        OO00OO00000O0O0OO =bytes (OOO0OOO0O0O0O000O .strftime ("%d/%m/%Y"),'utf-8')
        O0OO0000O0O0OO0OO =uuid .getnode ()
        OOOO0O00O0O00OO0O =base64 .encodebytes (bytes (str (O0OO0000O0O0OO0OO ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OO0OO000O00OOO0O0 .data +OOOO0O00O0O00OO0O )
            hash128_2 =hashlib .shake_256 (OO0OO000O00OOO0O0 .data +OOOO0O00O0O00OO0O )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (OO0OO000O00OOO0O0 .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOOO0O00O0O00OO0O ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        OOOOO00OO00O000O0 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OOO000O00OOOOOO00 =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O00OO0OO0000OO0O0 =OOOOO00OO00O000O0 +UUIDHASH128_3 .digest ()
        OOO0O0O0O0O0OOO0O =OOO000O00OOOOOO00 +UUIDHASH128_3 .hexdigest ()
        craxk_128_datemutation .digest_size =len (O00OO0OO0000OO0O0 )
        craxk_128_datemutation .block_size =len (OOO0O0O0O0O0OOO0O )
    def replace (OOO0O00OO00O00OOO ,OOO00O000OOOO0OOO =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OOO00O000OOOO0OOO ,(str ,int ,float ))!=True :
            OOO0O00OO00O00OOO .data =OOO00O000OOOO0OOO 
        else :
            OOO0O00OO00O00OOO .data =bytes (str (OOO00O000OOOO0OOO ),'utf-8')
        O00OO00OO0OOO0O0O =uuid .getnode ()
        OO0O0O0000O0O0OOO =base64 .encodebytes (bytes (str (O00OO00OO0OOO0O0O ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OOO0O00OO00O00OOO .data +OO0O0O0000O0O0OOO )
            hash128_2 =hashlib .shake_256 (OOO0O00OO00O00OOO .data +OO0O0O0000O0O0OOO )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (OOO0O00OO00O00OOO .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OO0O0O0000O0O0OOO ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        OO00OOO00O0O0OO00 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        O0OOOO00OO00OO00O =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O00O0OOOOO000OO0O =OO00OOO00O0O0OO00 +UUIDHASH128_3 .digest ()
        OOO0OO0OOO0000O0O =O0OOOO00OO00OO00O +UUIDHASH128_3 .hexdigest ()
        craxk_128 .digest_size =len (O00O0OOOOO000OO0O )
        craxk_128 .block_size =len (OOO0OO0OOO0000O0O )
    def hexdigest (O00O000O0OOOO0O0O ):
        OO000O0000O00OOOO =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        OO0O00O000O0O000O =OO000O0000O00OOOO +UUIDHASH128_3 .hexdigest ()
        return OO0O00O000O0O000O 
    def digest (O00000O00O0OOOO0O ):
        O0O0OO0000OO0O00O =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        O0000OOO00OO0OO00 =O0000OOO00OO0OO00 =O0O0OO0000OO0O00O +UUIDHASH128_3 .digest ()
        return O0000OOO00OO0OO00 
class craxk_128_datemutation ():
    digest_size =''
    block_size =''
    def __init__ (O00O0O00O00O00OO0 ,OOO0OO0O00O0O0OO0 =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OOO0OO0O00O0O0OO0 ,(str ,int ,float ))!=True :
            O00O0O00O00O00OO0 .data =OOO0OO0O00O0O0OO0 
        else :
            O00O0O00O00O00OO0 .data =bytes (str (OOO0OO0O00O0O0OO0 ),'utf-8')
        O0OO00O0OOOOOO00O =date .today ()
        OO0O00OOOO00O0OOO =bytes (O0OO00O0OOOOOO00O .strftime ("%d/%m/%Y"),'utf-8')
        OO00OO00OO0OOOO0O =uuid .getnode ()
        OOOO000OOOO00OOO0 =base64 .encodebytes (bytes (str (OO00OO00OO0OOOO0O ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O00O0O00O00O00OO0 .data +OOOO000OOOO00OOO0 +OO0O00OOOO00O0OOO )
            hash128_2 =hashlib .shake_256 (O00O0O00O00O00OO0 .data +OOOO000OOOO00OOO0 +OO0O00OOOO00O0OOO )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O00O0O00O00O00OO0 .data +OO0O00OOOO00O0OOO ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOOO000OOOO00OOO0 +OO0O00OOOO00O0OOO ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        O0OO00O0OOOOOOOOO =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OO00O0O0OO00OOO0O =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O0OO00000O00OOOO0 =O0OO00O0OOOOOOOOO +UUIDHASH128_3 .digest ()
        O00000OOO0OO0000O =OO00O0O0OO00OOO0O +UUIDHASH128_3 .hexdigest ()
        craxk_128_datemutation .digest_size =len (O0OO00000O00OOOO0 )
        craxk_128_datemutation .block_size =len (O00000OOO0OO0000O )
    def update (O0O0OOOOO0O00OO0O ,O00O0O0O0O000O0OO =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (O00O0O0O0O000O0OO ,(str ,int ,float ))!=True :
            O0O0OOOOO0O00OO0O .data =O0O0OOOOO0O00OO0O .data +O00O0O0O0O000O0OO 
        else :
            O0O0OOOOO0O00OO0O .data =O0O0OOOOO0O00OO0O .data +bytes (str (O00O0O0O0O000O0OO ),'utf-8')
        OO0OOOO0O0OO0OO0O =date .today ()
        OO0O000O0O0O00OO0 =bytes (OO0OOOO0O0OO0OO0O .strftime ("%d/%m/%Y"),'utf-8')
        OOOO00O00OO00000O =uuid .getnode ()
        OOOOO0OO0OOO00OOO =base64 .encodebytes (bytes (str (OOOO00O00OO00000O ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0O0OOOOO0O00OO0O .data +OOOOO0OO0OOO00OOO +OO0O000O0O0O00OO0 )
            hash128_2 =hashlib .shake_256 (O0O0OOOOO0O00OO0O .data +OOOOO0OO0OOO00OOO +OO0O000O0O0O00OO0 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O0O0OOOOO0O00OO0O .data +OO0O000O0O0O00OO0 ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOOOO0OO0OOO00OOO +OO0O000O0O0O00OO0 ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        OOO000O0O0OO00OOO =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OOOO000OOO0OO0O0O =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        OOOOOOOOOOOO0O00O =OOO000O0O0OO00OOO +UUIDHASH128_3 .digest ()
        OOO0O000OOO00O000 =OOOO000OOO0OO0O0O +UUIDHASH128_3 .hexdigest ()
        craxk_128_datemutation .digest_size =len (OOOOOOOOOOOO0O00O )
        craxk_128_datemutation .block_size =len (OOO0O000OOO00O000 )
    def replace (O0O00OO0O00OOOOO0 ,OOO0OOO00O00000OO =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OOO0OOO00O00000OO ,(str ,int ,float ))!=True :
            O0O00OO0O00OOOOO0 .data =OOO0OOO00O00000OO 
        else :
            O0O00OO0O00OOOOO0 .data =bytes (str (OOO0OOO00O00000OO ),'utf-8')
        OOOOO0OOO0O00000O =date .today ()
        O00OO0OOO0OO0OO00 =bytes (OOOOO0OOO0O00000O .strftime ("%d/%m/%Y"),'utf-8')
        O0O00O0000OOOO0O0 =uuid .getnode ()
        O0OO0O0OOOO000O00 =base64 .encodebytes (bytes (str (O0O00O0000OOOO0O0 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0O00OO0O00OOOOO0 .data +O0OO0O0OOOO000O00 )
            hash128_2 =hashlib .shake_256 (O0O00OO0O00OOOOO0 .data +O0OO0O0OOOO000O00 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O0O00OO0O00OOOOO0 .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (O0OO0O0OOOO000O00 ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        OO0O0OO00O0OOO00O =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OO000O00O0O0OO00O =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O00O0O00OOO0OO00O =OO0O0OO00O0OOO00O +UUIDHASH128_3 .digest ()
        OOOO0O000OOO00O0O =OO000O00O0O0OO00O +UUIDHASH128_3 .hexdigest ()
        craxk_128_datemutation .digest_size =len (O00O0O00OOO0OO00O )
        craxk_128_datemutation .block_size =len (OOOO0O000OOO00O0O )
    def hexdigest (O0000OOOOO00OOO0O ):
        O0O00O00O0OOOOOOO =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O0OOO0OO000O00OO0 =O0O00O00O0OOOOOOO +UUIDHASH128_3 .hexdigest ()
        return O0OOO0OO000O00OO0 
    def digest (O000OOO000000OOO0 ):
        O000OOO0OO00OOOOO =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OO000O0O0O0O0O0OO =OO000O0O0O0O0O0OO =O000OOO0OO00OOOOO +UUIDHASH128_3 .digest ()
        return OO000O0O0O0O0O0OO 
class craxk_128_seedmutation ():
    digest_size =''
    block_size =''
    def __init__ (OO00OO0O00O00OOO0 ,O0O0OO0000OOO0O00 ='',O0O00OOOOOOOO0O0O =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if O0O00OOOOOOOO0O0O =='':
            print ("ExceptCode 202")
            print ("TypeError: The seed is mandatory and cannot be a blank space.")
            exit ()
        if isinstance (O0O0OO0000OOO0O00 ,(str ,int ,float ))!=True :
            OO00OO0O00O00OOO0 .data =O0O0OO0000OOO0O00 
        else :
            OO00OO0O00O00OOO0 .data =bytes (str (O0O0OO0000OOO0O00 ),'utf-8')
        if isinstance (O0O00OOOOOOOO0O0O ,bytes )==True :
            OO00OO0O00O00OOO0 .seed =O0O00OOOOOOOO0O0O 
        else :
            OO00OO0O00O00OOO0 .seed =bytes (str (O0O00OOOOOOOO0O0O ),'utf-8')
        OOOOO0O0O0O0O00OO =uuid .getnode ()
        O0OO0O0OO0OO00O00 =base64 .encodebytes (bytes (str (OOOOO0O0O0O0O00OO ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OO00OO0O00O00OOO0 .data +O0OO0O0OO0OO00O00 +OO00OO0O00O00OOO0 .seed )
            hash128_2 =hashlib .shake_256 (OO00OO0O00O00OOO0 .data +O0OO0O0OO0OO00O00 +OO00OO0O00O00OOO0 .seed )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (OO00OO0O00O00OOO0 .data +OO00OO0O00O00OOO0 .seed ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (O0OO0O0OO0OO00O00 +OO00OO0O00O00OOO0 .seed ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        O0O0O0O0OOO000O00 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        O0O0O0OO00O0O000O =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O0OO00O00O0OOOOOO =O0O0O0O0OOO000O00 +UUIDHASH128_3 .digest ()
        OO0O00OO0000OOO0O =O0O0O0OO00O0O000O +UUIDHASH128_3 .hexdigest ()
        craxk_128_seedmutation .digest_size =len (O0OO00O00O0OOOOOO )
        craxk_128_seedmutation .block_size =len (OO0O00OO0000OOO0O )
    def update (O0OOOO00OOO00OO0O ,OO00O0O0O0OO00000 =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OO00O0O0O0OO00000 ,(str ,int ,float ))!=True :
            O0OOOO00OOO00OO0O .data =O0OOOO00OOO00OO0O .data +OO00O0O0O0OO00000 
        else :
            O0OOOO00OOO00OO0O .data =O0OOOO00OOO00OO0O .data +bytes (str (OO00O0O0O0OO00000 ),'utf-8')
        OO00OO0000O00O0OO =uuid .getnode ()
        OOOOO00OO00O00OO0 =base64 .encodebytes (bytes (str (OO00OO0000O00O0OO ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0OOOO00OOO00OO0O .data +OOOOO00OO00O00OO0 +O0OOOO00OOO00OO0O .seed )
            hash128_2 =hashlib .shake_256 (O0OOOO00OOO00OO0O .data +OOOOO00OO00O00OO0 +O0OOOO00OOO00OO0O .seed )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O0OOOO00OOO00OO0O .data +O0OOOO00OOO00OO0O .seed ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOOOO00OO00O00OO0 +O0OOOO00OOO00OO0O .seed ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        OO0OOO0O00OO0OOO0 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        O0OO0OO0OO0O0O000 =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O0O0000000OOOOOO0 =OO0OOO0O00OO0OOO0 +UUIDHASH128_3 .digest ()
        O0OO0OO0000O00OOO =O0OO0OO0OO0O0O000 +UUIDHASH128_3 .hexdigest ()
        craxk_128_seedmutation .digest_size =len (O0O0000000OOOOOO0 )
        craxk_128_seedmutation .block_size =len (O0OO0OO0000O00OOO )
    def replace (OO0OO0OOOO0O0OO0O ,OOOO00O0O0OO00O00 ='',O0O0OOOO0OOOO0OO0 =''):
        if O0O0OOOO0OOOO0OO0 =='':
            print ("ExceptCode 202")
            print ("TypeError: The seed is mandatory and cannot be a blank space.")
            exit ()
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OOOO00O0O0OO00O00 ,(str ,int ,float ))!=True :
            OO0OO0OOOO0O0OO0O .data =OOOO00O0O0OO00O00 
        else :
            OO0OO0OOOO0O0OO0O .data =bytes (str (OOOO00O0O0OO00O00 ),'utf-8')
        if isinstance (O0O0OOOO0OOOO0OO0 ,str )==True :
            O0O0OOOO0OOOO0OO0 =bytes (O0O0OOOO0OOOO0OO0 ,'utf-8')
        else :
            pass 
        O00OOOOO00OO000OO =uuid .getnode ()
        O0000O000OO00000O =base64 .encodebytes (bytes (str (O00OOOOO00OO000OO ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OO0OO0OOOO0O0OO0O .data +O0000O000OO00000O +O0O0OOOO0OOOO0OO0 )
            hash128_2 =hashlib .shake_256 (OO0OO0OOOO0O0OO0O .data +O0000O000OO00000O +O0O0OOOO0OOOO0OO0 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (OO0OO0OOOO0O0OO0O .data +O0O0OOOO0OOOO0OO0 ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (O0000O000OO00000O +O0O0OOOO0OOOO0OO0 ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        OO00O0000O0O0O000 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OO000O00000O0O0O0 =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        OO0O00O0O0OOOOOOO =OO00O0000O0O0O000 +UUIDHASH128_3 .digest ()
        OOOO0O0OO00O0OOO0 =OO000O00000O0O0O0 +UUIDHASH128_3 .hexdigest ()
        craxk_128_seedmutation .digest_size =len (OO0O00O0O0OOOOOOO )
        craxk_128_seedmutation .block_size =len (OOOO0O0OO00O0OOO0 )
    def hexdigest (O0OOO0OOO0O00O0O0 ):
        OO00OO0O000O00O0O =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        OOOOO000OOOO00O0O =OO00OO0O000O00O0O +UUIDHASH128_3 .hexdigest ()
        return OOOOO000OOOO00O0O 
    def digest (OOO0OO000OOOOOOOO ):
        O0O0OO00O0O00OOOO =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        O000OOO0O000OO0O0 =O000OOO0O000OO0O0 =O0O0OO00O0O00OOOO +UUIDHASH128_3 .digest ()
        return O000OOO0O000OO0O0 
class craxk_256 ():
    digest_size =''
    block_size =''
    def __init__ (OOO0O00O00OOOO0O0 ,O0000OOOO0000OO0O =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (O0000OOOO0000OO0O ,(str ,int ,float ))!=True :
            OOO0O00O00OOOO0O0 .data =O0000OOOO0000OO0O 
        else :
            OOO0O00O00OOOO0O0 .data =bytes (str (O0000OOOO0000OO0O ),'utf-8')
        O0O000000OO0O0000 =uuid .getnode ()
        O0O00O00O0000O000 =base64 .encodebytes (bytes (str (O0O000000OO0O0000 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OOO0O00O00OOOO0O0 .data +O0O00O00O0000O000 )
            hash128_2 =hashlib .shake_256 (OOO0O00O00OOOO0O0 .data +O0O00O00O0000O000 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (OOO0O00O00OOOO0O0 .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (O0O00O00O0000O000 ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =18 )
        O000O0000000000O0 =hash128_1 .digest (6 )+hash128_2 .digest (8 )
        OO0O0000O00000OOO =hash128_1 .hexdigest (6 )+hash128_2 .hexdigest (8 )
        OOO0OO0O0OO00O000 =O000O0000000000O0 +UUIDHASH128_3 .digest ()
        OOOO0OOOOO0OOOOO0 =OO0O0000O00000OOO +UUIDHASH128_3 .hexdigest ()
        craxk_256 .digest_size =len (OOO0OO0O0OO00O000 )
        craxk_256 .block_size =len (OOOO0OOOOO0OOOOO0 )
    def update (O0OOOOO000O00OOOO ,O0OO00O0OOO000OO0 =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (O0OO00O0OOO000OO0 ,(str ,int ,float ))!=True :
            O0OOOOO000O00OOOO .data =O0OOOOO000O00OOOO .data +O0OO00O0OOO000OO0 
        else :
            O0OOOOO000O00OOOO .data =O0OOOOO000O00OOOO .data +bytes (str (O0OO00O0OOO000OO0 ),'utf-8')
        O0OO0OO0O0O00OO00 =date .today ()
        O00OO0OOOO000O00O =bytes (O0OO0OO0O0O00OO00 .strftime ("%d/%m/%Y"),'utf-8')
        OOOOO0OOO000OOOO0 =uuid .getnode ()
        OOOOOO0O0000O0OOO =base64 .encodebytes (bytes (str (OOOOO0OOO000OOOO0 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0OOOOO000O00OOOO .data +OOOOOO0O0000O0OOO )
            hash128_2 =hashlib .shake_256 (O0OOOOO000O00OOOO .data +OOOOOO0O0000O0OOO )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O0OOOOO000O00OOOO .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOOOOO0O0000O0OOO ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =18 )
        OO00O00OO000OOOO0 =hash128_1 .digest (6 )+hash128_2 .digest (8 )
        O0OOO0O00O0OOOOO0 =hash128_1 .hexdigest (6 )+hash128_2 .hexdigest (8 )
        O0O0OO0000O00OOO0 =OO00O00OO000OOOO0 +UUIDHASH128_3 .digest ()
        O0OO0OOO0000O00OO =O0OOO0O00O0OOOOO0 +UUIDHASH128_3 .hexdigest ()
        craxk_256_datemutation .digest_size =len (O0O0OO0000O00OOO0 )
        craxk_256_datemutation .block_size =len (O0OO0OOO0000O00OO )
    def replace (O0000O000O000OOO0 ,OO0O0000OOO0O000O =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OO0O0000OOO0O000O ,(str ,int ,float ))!=True :
            O0000O000O000OOO0 .data =OO0O0000OOO0O000O 
        else :
            O0000O000O000OOO0 .data =bytes (str (OO0O0000OOO0O000O ),'utf-8')
        O0O00O00OOOOOO000 =uuid .getnode ()
        OOOOO000OOOOOO0OO =base64 .encodebytes (bytes (str (O0O00O00OOOOOO000 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0000O000O000OOO0 .data +OOOOO000OOOOOO0OO )
            hash128_2 =hashlib .shake_256 (O0000O000O000OOO0 .data +OOOOO000OOOOOO0OO )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O0000O000O000OOO0 .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOOOO000OOOOOO0OO ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        O00O0O00O0000OO00 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OOO0OO0OOO0O0OOOO =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O0OO000O00OOO0000 =O00O0O00O0000OO00 +UUIDHASH128_3 .digest ()
        OO000OOO0OOO0OOOO =OOO0OO0OOO0O0OOOO +UUIDHASH128_3 .hexdigest ()
        craxk_256 .digest_size =len (O0OO000O00OOO0000 )
        craxk_256 .block_size =len (OO000OOO0OOO0OOOO )
    def hexdigest (OOO0OO0OOO000OOOO ):
        OOOOO00O0OOOOOOOO =hash128_1 .hexdigest (6 )+hash128_2 .hexdigest (8 )
        OO00O0OOOOO0O0O0O =OOOOO00O0OOOOOOOO +UUIDHASH128_3 .hexdigest ()
        return OO00O0OOOOO0O0O0O 
    def digest (OOO00O000O0O000OO ):
        OOOO0O0000O0O0O0O =hash128_1 .digest (6 )+hash128_2 .digest (8 )
        OOOO00OOOO0000O00 =OOOO00OOOO0000O00 =OOOO0O0000O0O0O0O +UUIDHASH128_3 .digest ()
        return OOOO00OOOO0000O00 
class craxk_256_datemutation ():
    digest_size =''
    block_size =''
    def __init__ (O00OOOOOOO00OOO0O ,OO00O00O000000OO0 =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OO00O00O000000OO0 ,(str ,int ,float ))!=True :
            O00OOOOOOO00OOO0O .data =OO00O00O000000OO0 
        else :
            O00OOOOOOO00OOO0O .data =bytes (str (OO00O00O000000OO0 ),'utf-8')
        O0O00OOOOO0000OOO =date .today ()
        O0OO0OO0O0O0O0000 =bytes (O0O00OOOOO0000OOO .strftime ("%d/%m/%Y"),'utf-8')
        O00OOOOO0O000OOO0 =uuid .getnode ()
        OOO0O00O000OOOOOO =base64 .encodebytes (bytes (str (O00OOOOO0O000OOO0 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O00OOOOOOO00OOO0O .data +OOO0O00O000OOOOOO +O0OO0OO0O0O0O0000 )
            hash128_2 =hashlib .shake_256 (O00OOOOOOO00OOO0O .data +OOO0O00O000OOOOOO +O0OO0OO0O0O0O0000 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O00OOOOOOO00OOO0O .data +O0OO0OO0O0O0O0000 ,digest_size =18 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOO0O00O000OOOOOO +O0OO0OO0O0O0O0000 ,digest_size =18 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =18 )
        O00O0O00000000O0O =hash128_1 .digest (6 )+hash128_2 .digest (8 )
        OOO0OOOO00OOOO0O0 =hash128_1 .hexdigest (6 )+hash128_2 .hexdigest (8 )
        O0O0O00O0OO00OOOO =O00O0O00000000O0O +UUIDHASH128_3 .digest ()
        OOOO0O0O00O0OO00O =OOO0OOOO00OOOO0O0 +UUIDHASH128_3 .hexdigest ()
        craxk_256_datemutation .digest_size =len (O0O0O00O0OO00OOOO )
        craxk_256_datemutation .block_size =len (OOOO0O0O00O0OO00O )
    def update (O00O0OO00O00O0000 ,OOOOOOO0OOOOOO0OO =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OOOOOOO0OOOOOO0OO ,(str ,int ,float ))!=True :
            O00O0OO00O00O0000 .data =O00O0OO00O00O0000 .data +OOOOOOO0OOOOOO0OO 
        else :
            O00O0OO00O00O0000 .data =O00O0OO00O00O0000 .data +bytes (str (OOOOOOO0OOOOOO0OO ),'utf-8')
        OOOOO0OO0000O00OO =date .today ()
        O00O00OOOO0O00O00 =bytes (OOOOO0OO0000O00OO .strftime ("%d/%m/%Y"),'utf-8')
        O0O0OOOOOO0OOO000 =uuid .getnode ()
        OOO0O0O00OOO000O0 =base64 .encodebytes (bytes (str (O0O0OOOOOO0OOO000 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O00O0OO00O00O0000 .data +OOO0O0O00OOO000O0 +O00O00OOOO0O00O00 )
            hash128_2 =hashlib .shake_256 (O00O0OO00O00O0000 .data +OOO0O0O00OOO000O0 +O00O00OOOO0O00O00 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O00O0OO00O00O0000 .data +O00O00OOOO0O00O00 ,digest_size =18 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOO0O0O00OOO000O0 +O00O00OOOO0O00O00 ,digest_size =18 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =18 )
        O000OOO00000OO00O =hash128_1 .digest (6 )+hash128_2 .digest (8 )
        O0OO0000OO0OOO0O0 =hash128_1 .hexdigest (6 )+hash128_2 .hexdigest (8 )
        OO00O00000O0OO0OO =O000OOO00000OO00O +UUIDHASH128_3 .digest ()
        O0O000OO0OOO000OO =O0OO0000OO0OOO0O0 +UUIDHASH128_3 .hexdigest ()
        craxk_256_datemutation .digest_size =len (OO00O00000O0OO0OO )
        craxk_256_datemutation .block_size =len (O0O000OO0OOO000OO )
    def replace (O00O00000O00OO0O0 ,O0O00O0O0OOOO0OO0 =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (O0O00O0O0OOOO0OO0 ,(str ,int ,float ))!=True :
            O00O00000O00OO0O0 .data =O0O00O0O0OOOO0OO0 
        else :
            O00O00000O00OO0O0 .data =bytes (str (O0O00O0O0OOOO0OO0 ),'utf-8')
        OOO0OO0000OOOOOOO =date .today ()
        OO0OOOO0OO0OOO0OO =bytes (OOO0OO0000OOOOOOO .strftime ("%d/%m/%Y"),'utf-8')
        OO0O00OO000O0OO0O =uuid .getnode ()
        O00000O000O0O000O =base64 .encodebytes (bytes (str (OO0O00OO000O0OO0O ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O00O00000O00OO0O0 .data +O00000O000O0O000O )
            hash128_2 =hashlib .shake_256 (O00O00000O00OO0O0 .data +O00000O000O0O000O )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O00O00000O00OO0O0 .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (O00000O000O0O000O ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        OO0OOO0O00O00O0O0 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OOO00O0O00O000OO0 =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O0OO0O00O0O00OOO0 =OO0OOO0O00O00O0O0 +UUIDHASH128_3 .digest ()
        O000O0O0OOOO00000 =OOO00O0O00O000OO0 +UUIDHASH128_3 .hexdigest ()
        craxk_256_datemutation .digest_size =len (O0OO0O00O0O00OOO0 )
        craxk_256_datemutation .block_size =len (O000O0O0OOOO00000 )
    def hexdigest (O0O00O00OOOO0OO0O ):
        O0OOO0000000O0O0O =hash128_1 .hexdigest (6 )+hash128_2 .hexdigest (8 )
        O000O00OO0OOO00O0 =O0OOO0000000O0O0O +UUIDHASH128_3 .hexdigest ()
        return O000O00OO0OOO00O0 
    def digest (OOOO00O00O00OO00O ):
        OOO0O0OOO000O000O =hash128_1 .digest (6 )+hash128_2 .digest (8 )
        OO00O0OOO00O00OOO =OO00O0OOO00O00OOO =OOO0O0OOO000O000O +UUIDHASH128_3 .digest ()
        return OO00O0OOO00O00OOO 
class craxk_256_seedmutation ():
    digest_size =''
    block_size =''
    def __init__ (OO0000OO00OOO0OOO ,OO0O0OO0O0OO0O0O0 ='',O00OO00000OOOO00O =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if O00OO00000OOOO00O =='':
            print ("ExceptCode 202")
            print ("TypeError: The seed is mandatory and cannot be a blank space.")
            exit ()
        if isinstance (OO0O0OO0O0OO0O0O0 ,(str ,int ,float ))!=True :
            OO0000OO00OOO0OOO .data =OO0O0OO0O0OO0O0O0 
        else :
            OO0000OO00OOO0OOO .data =bytes (str (OO0O0OO0O0OO0O0O0 ),'utf-8')
        if isinstance (O00OO00000OOOO00O ,bytes )==True :
            OO0000OO00OOO0OOO .seed =O00OO00000OOOO00O 
        else :
            OO0000OO00OOO0OOO .seed =bytes (O00OO00000OOOO00O ,'utf-8')
        O0OOO0O000OO000OO =uuid .getnode ()
        OO00O00O0OOO000OO =base64 .encodebytes (bytes (str (O0OOO0O000OO000OO ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OO0000OO00OOO0OOO .data +OO00O00O0OOO000OO +OO0000OO00OOO0OOO .seed )
            hash128_2 =hashlib .shake_256 (OO0000OO00OOO0OOO .data +OO00O00O0OOO000OO +OO0000OO00OOO0OOO .seed )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (OO0000OO00OOO0OOO .data +OO0000OO00OOO0OOO .seed ,digest_size =18 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OO00O00O0OOO000OO +OO0000OO00OOO0OOO .seed ,digest_size =18 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =18 )
        OO000O0000O0O0OO0 =hash128_1 .digest (6 )+hash128_2 .digest (8 )
        O0OO0O0OOO0000000 =hash128_1 .hexdigest (6 )+hash128_2 .hexdigest (8 )
        OOOO0OO000OO0O0OO =OO000O0000O0O0OO0 +UUIDHASH128_3 .digest ()
        O0OOO0OOO0OO0000O =O0OO0O0OOO0000000 +UUIDHASH128_3 .hexdigest ()
        craxk_256_seedmutation .digest_size =len (OOOO0OO000OO0O0OO )
        craxk_256_seedmutation .block_size =len (O0OOO0OOO0OO0000O )
    def update (O00000OO0O0O0O000 ,OOOO0OOO000O00OOO =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OOOO0OOO000O00OOO ,(str ,int ,float ))!=True :
            O00000OO0O0O0O000 .data =O00000OO0O0O0O000 .data +OOOO0OOO000O00OOO 
        else :
            O00000OO0O0O0O000 .data =O00000OO0O0O0O000 .data +bytes (str (OOOO0OOO000O00OOO ),'utf-8')
        O0O0OOO00000O0000 =uuid .getnode ()
        OO00OOO0OOOOO0O0O =base64 .encodebytes (bytes (str (O0O0OOO00000O0000 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O00000OO0O0O0O000 .data +OO00OOO0OOOOO0O0O +O00000OO0O0O0O000 .seed )
            hash128_2 =hashlib .shake_256 (O00000OO0O0O0O000 .data +OO00OOO0OOOOO0O0O +O00000OO0O0O0O000 .seed )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O00000OO0O0O0O000 .data +O00000OO0O0O0O000 .seed ,digest_size =18 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OO00OOO0OOOOO0O0O +O00000OO0O0O0O000 .seed ,digest_size =18 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =18 )
        O000000OO000OOO00 =hash128_1 .digest (6 )+hash128_2 .digest (8 )
        O00000000O000OO0O =hash128_1 .hexdigest (6 )+hash128_2 .hexdigest (8 )
        OO0O00OO000OOOOOO =O000000OO000OOO00 +UUIDHASH128_3 .digest ()
        OOO0O0OO000O0OO0O =O00000000O000OO0O +UUIDHASH128_3 .hexdigest ()
        craxk_256_seedmutation .digest_size =len (OO0O00OO000OOOOOO )
        craxk_256_seedmutation .block_size =len (OOO0O0OO000O0OO0O )
    def replace (O0OOOOO0O0O0000O0 ,OOO0O0000OOO000O0 ='',OOO0O00O0O000000O =''):
        if OOO0O00O0O000000O =='':
            print ("ExceptCode 202")
            print ("TypeError: The seed is mandatory and cannot be a blank space.")
            exit ()
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OOO0O0000OOO000O0 ,(str ,int ,float ))!=True :
            O0OOOOO0O0O0000O0 .data =OOO0O0000OOO000O0 
        else :
            O0OOOOO0O0O0000O0 .data =bytes (str (OOO0O0000OOO000O0 ),'utf-8')
        if isinstance (OOO0O00O0O000000O ,str )==True :
            OOO0O00O0O000000O =bytes (OOO0O00O0O000000O ,'utf-8')
        else :
            pass 
        OOO0O0000OOO0OOOO =uuid .getnode ()
        OOO0OO0OOO0O000O0 =base64 .encodebytes (bytes (str (OOO0O0000OOO0OOOO ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0OOOOO0O0O0000O0 .data +OOO0OO0OOO0O000O0 +OOO0O00O0O000000O )
            hash128_2 =hashlib .shake_256 (O0OOOOO0O0O0000O0 .data +OOO0OO0OOO0O000O0 +OOO0O00O0O000000O )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O0OOOOO0O0O0000O0 .data +OOO0O00O0O000000O ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOO0OO0OOO0O000O0 +OOO0O00O0O000000O ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        OO0O00O0OO0000O00 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        O00OOO00000OOO0O0 =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        OO00OOO0OOO0O00O0 =OO0O00O0OO0000O00 +UUIDHASH128_3 .digest ()
        OOO00OO00O000O00O =O00OOO00000OOO0O0 +UUIDHASH128_3 .hexdigest ()
        craxk_256_seedmutation .digest_size =len (OO00OOO0OOO0O00O0 )
        craxk_256_seedmutation .block_size =len (OOO00OO00O000O00O )
    def hexdigest (O0OO0OOOO0000000O ):
        O00OO0OOO00O0O000 =hash128_1 .hexdigest (6 )+hash128_2 .hexdigest (8 )
        O000O00OOO00OOO0O =O00OO0OOO00O0O000 +UUIDHASH128_3 .hexdigest ()
        return O000O00OOO00OOO0O 
    def digest (O0OOO0O00O0000OOO ):
        OOO0O0OOOOOOO000O =hash128_1 .digest (6 )+hash128_2 .digest (8 )
        OOO0O0O0OOOOOOO0O =OOO0O0O0OOOOOOO0O =OOO0O0OOOOOOO000O +UUIDHASH128_3 .digest ()
        return OOO0O0O0OOOOOOO0O 
class craxk_512 ():
    digest_size =''
    block_size =''
    def __init__ (O0OO00O0OO00OOOOO ,OOOO000OOO00O000O =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OOOO000OOO00O000O ,(str ,int ,float ))!=True :
            O0OO00O0OO00OOOOO .data =OOOO000OOO00O000O 
        else :
            O0OO00O0OO00OOOOO .data =bytes (str (OOOO000OOO00O000O ),'utf-8')
        O0O0OO0OO00O0OO0O =uuid .getnode ()
        OO0000OOO000OOO00 =base64 .encodebytes (bytes (str (O0O0OO0OO00O0OO0O ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0OO00O0OO00OOOOO .data +OO0000OOO000OOO00 )
            hash128_2 =hashlib .shake_256 (O0OO00O0OO00OOOOO .data +OO0000OOO000OOO00 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2b (O0OO00O0OO00OOOOO .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2b (OO0000OOO000OOO00 ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2b (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =34 )
        OOO0O0OOO00000O0O =hash128_1 .digest (14 )+hash128_2 .digest (16 )
        OOOO0O00O000O0O00 =hash128_1 .hexdigest (14 )+hash128_2 .hexdigest (16 )
        O000O0000OO0O000O =OOO0O0OOO00000O0O +UUIDHASH128_3 .digest ()
        O0OO0OO0000OOO0OO =OOOO0O00O000O0O00 +UUIDHASH128_3 .hexdigest ()
        craxk_512 .digest_size =len (O000O0000OO0O000O )
        craxk_512 .block_size =len (O0OO0OO0000OOO0OO )
    def update (OO0OO000O0OOOOOOO ,OO000OOO00000OO0O =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OO000OOO00000OO0O ,(str ,int ,float ))!=True :
            OO0OO000O0OOOOOOO .data =OO0OO000O0OOOOOOO .data +OO000OOO00000OO0O 
        else :
            OO0OO000O0OOOOOOO .data =OO0OO000O0OOOOOOO .data +bytes (str (OO000OOO00000OO0O ),'utf-8')
        O0OO000O00000OOOO =date .today ()
        OO00OOO0OO0O0O0O0 =bytes (O0OO000O00000OOOO .strftime ("%d/%m/%Y"),'utf-8')
        OOO00O000OO0OO000 =uuid .getnode ()
        OO0O0000OO00OOO0O =base64 .encodebytes (bytes (str (OOO00O000OO0OO000 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OO0OO000O0OOOOOOO .data +OO0O0000OO00OOO0O )
            hash128_2 =hashlib .shake_256 (OO0OO000O0OOOOOOO .data +OO0O0000OO00OOO0O )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2b (OO0OO000O0OOOOOOO .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2b (OO0O0000OO00OOO0O ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2b (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =34 )
        OO00000OO0OO00OO0 =hash128_1 .digest (14 )+hash128_2 .digest (16 )
        OO0O000OOO000OO00 =hash128_1 .hexdigest (14 )+hash128_2 .hexdigest (16 )
        OO0O0O000OO0OO0O0 =OO00000OO0OO00OO0 +UUIDHASH128_3 .digest ()
        OOO0O0OO0O0O00000 =OO0O000OOO000OO00 +UUIDHASH128_3 .hexdigest ()
        craxk_512_datemutation .digest_size =len (OO0O0O000OO0OO0O0 )
        craxk_512_datemutation .block_size =len (OOO0O0OO0O0O00000 )
    def replace (OO0OO0O00OO00000O ,OO000OOOOO0O0OOOO =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OO000OOOOO0O0OOOO ,(str ,int ,float ))!=True :
            OO0OO0O00OO00000O .data =OO000OOOOO0O0OOOO 
        else :
            OO0OO0O00OO00000O .data =bytes (str (OO000OOOOO0O0OOOO ),'utf-8')
        OO00OOO000OO0O000 =uuid .getnode ()
        O0OO0O000OO0OO0O0 =base64 .encodebytes (bytes (str (OO00OOO000OO0O000 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OO0OO0O00OO00000O .data +O0OO0O000OO0OO0O0 )
            hash128_2 =hashlib .shake_256 (OO0OO0O00OO00000O .data +O0OO0O000OO0OO0O0 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (OO0OO0O00OO00000O .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (O0OO0O000OO0OO0O0 ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        OOO00O00OO00O0000 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OO00OOOOOOO000OOO =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        OO0OOOOOO0OO00000 =OOO00O00OO00O0000 +UUIDHASH128_3 .digest ()
        OOO0O0OOO000O0O00 =OO00OOOOOOO000OOO +UUIDHASH128_3 .hexdigest ()
        craxk_512 .digest_size =len (OO0OOOOOO0OO00000 )
        craxk_512 .block_size =len (OOO0O0OOO000O0O00 )
    def hexdigest (OOO0OOOO00000O000 ):
        O0O00OOOOO000OOOO =hash128_1 .hexdigest (14 )+hash128_2 .hexdigest (16 )
        OOO0O00O000000000 =O0O00OOOOO000OOOO +UUIDHASH128_3 .hexdigest ()
        return OOO0O00O000000000 
    def digest (OOO00OOO0O0O0OOOO ):
        O000000O00OOO0O00 =hash128_1 .digest (14 )+hash128_2 .digest (16 )
        OOOO0O0000O00OOO0 =OOOO0O0000O00OOO0 =O000000O00OOO0O00 +UUIDHASH128_3 .digest ()
        return OOOO0O0000O00OOO0 
class craxk_512_datemutation ():
    digest_size =''
    block_size =''
    def __init__ (OOOO0O0OOO0O0000O ,O0OO0OOO0OOO0OO00 =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (O0OO0OOO0OOO0OO00 ,(str ,int ,float ))!=True :
            OOOO0O0OOO0O0000O .data =O0OO0OOO0OOO0OO00 
        else :
            OOOO0O0OOO0O0000O .data =bytes (str (O0OO0OOO0OOO0OO00 ),'utf-8')
        O00OOOOO0O00OOOOO =date .today ()
        OOO000OO0OOO00OOO =bytes (O00OOOOO0O00OOOOO .strftime ("%d/%m/%Y"),'utf-8')
        OO0O00OOO0000000O =uuid .getnode ()
        OO0O000000O0O0O00 =base64 .encodebytes (bytes (str (OO0O00OOO0000000O ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OOOO0O0OOO0O0000O .data +OO0O000000O0O0O00 +OOO000OO0OOO00OOO )
            hash128_2 =hashlib .shake_256 (OOOO0O0OOO0O0000O .data +OO0O000000O0O0O00 +OOO000OO0OOO00OOO )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2b (OOOO0O0OOO0O0000O .data +OOO000OO0OOO00OOO ,digest_size =34 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2b (OO0O000000O0O0O00 +OOO000OO0OOO00OOO ,digest_size =34 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2b (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =34 )
        O000OO0O0OOOOOO0O =hash128_1 .digest (14 )+hash128_2 .digest (16 )
        O00OOOO0000O000O0 =hash128_1 .hexdigest (14 )+hash128_2 .hexdigest (16 )
        OOO0OOO00OOO0000O =O000OO0O0OOOOOO0O +UUIDHASH128_3 .digest ()
        O0O0OO00O000O0OOO =O00OOOO0000O000O0 +UUIDHASH128_3 .hexdigest ()
        craxk_512_datemutation .digest_size =len (OOO0OOO00OOO0000O )
        craxk_512_datemutation .block_size =len (O0O0OO00O000O0OOO )
    def update (OOO00O00O0O0000OO ,OO0OOO00O0OOOO00O =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OO0OOO00O0OOOO00O ,(str ,int ,float ))!=True :
            OOO00O00O0O0000OO .data =OOO00O00O0O0000OO .data +OO0OOO00O0OOOO00O 
        else :
            OOO00O00O0O0000OO .data =OOO00O00O0O0000OO .data +bytes (str (OO0OOO00O0OOOO00O ),'utf-8')
        OO0O0OO0OOOO0O000 =date .today ()
        O0O00OO0O00O0OOOO =bytes (OO0O0OO0OOOO0O000 .strftime ("%d/%m/%Y"),'utf-8')
        OOOOOOO00OO000000 =uuid .getnode ()
        O0O00O0000O00OO00 =base64 .encodebytes (bytes (str (OOOOOOO00OO000000 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OOO00O00O0O0000OO .data +O0O00O0000O00OO00 +O0O00OO0O00O0OOOO )
            hash128_2 =hashlib .shake_256 (OOO00O00O0O0000OO .data +O0O00O0000O00OO00 +O0O00OO0O00O0OOOO )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2b (OOO00O00O0O0000OO .data +O0O00OO0O00O0OOOO ,digest_size =34 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2b (O0O00O0000O00OO00 +O0O00OO0O00O0OOOO ,digest_size =34 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2b (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =34 )
        O00O0O0O0O0000000 =hash128_1 .digest (14 )+hash128_2 .digest (16 )
        O000OOOOOO00OOO00 =hash128_1 .hexdigest (14 )+hash128_2 .hexdigest (16 )
        OO000O0OO000O00O0 =O00O0O0O0O0000000 +UUIDHASH128_3 .digest ()
        O00OOOO0OO0OOOOO0 =O000OOOOOO00OOO00 +UUIDHASH128_3 .hexdigest ()
        craxk_512_datemutation .digest_size =len (OO000O0OO000O00O0 )
        craxk_512_datemutation .block_size =len (O00OOOO0OO0OOOOO0 )
    def replace (O0OO00O000OO0000O ,OO0OOO0OO00OOO0O0 =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OO0OOO0OO00OOO0O0 ,(str ,int ,float ))!=True :
            O0OO00O000OO0000O .data =OO0OOO0OO00OOO0O0 
        else :
            O0OO00O000OO0000O .data =bytes (str (OO0OOO0OO00OOO0O0 ),'utf-8')
        O00OO0O00O0000OO0 =date .today ()
        O000O0O0O000O0000 =bytes (O00OO0O00O0000OO0 .strftime ("%d/%m/%Y"),'utf-8')
        O0O0O000O000O0O0O =uuid .getnode ()
        OO0O0OOOOO0000O00 =base64 .encodebytes (bytes (str (O0O0O000O000O0O0O ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0OO00O000OO0000O .data +OO0O0OOOOO0000O00 )
            hash128_2 =hashlib .shake_256 (O0OO00O000OO0000O .data +OO0O0OOOOO0000O00 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O0OO00O000OO0000O .data ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OO0O0OOOOO0000O00 ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        O000OO000OOOO00OO =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OOO00OOO00OO0O000 =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O00OOOO000O0OOOO0 =O000OO000OOOO00OO +UUIDHASH128_3 .digest ()
        O0000O0000000OOO0 =OOO00OOO00OO0O000 +UUIDHASH128_3 .hexdigest ()
        craxk_512_datemutation .digest_size =len (O00OOOO000O0OOOO0 )
        craxk_512_datemutation .block_size =len (O0000O0000000OOO0 )
    def hexdigest (O0000OO0000OOO00O ):
        O00O0OOOO0O0OO000 =hash128_1 .hexdigest (14 )+hash128_2 .hexdigest (16 )
        O00O000OOOO00OOOO =O00O0OOOO0O0OO000 +UUIDHASH128_3 .hexdigest ()
        return O00O000OOOO00OOOO 
    def digest (OOO0OO00O000O0000 ):
        O00OOOOO0O0O00OO0 =hash128_1 .digest (14 )+hash128_2 .digest (16 )
        O0O00O00OO00000O0 =O0O00O00OO00000O0 =O00OOOOO0O0O00OO0 +UUIDHASH128_3 .digest ()
        return O0O00O00OO00000O0 
class craxk_512_seedmutation ():
    digest_size =''
    block_size =''
    def __init__ (OO000OOO0OO000OOO ,O000OO0O0O0OO0000 ='',OO000OOO0O0O0O0OO =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if OO000OOO0O0O0O0OO =='':
            print ("ExceptCode 202")
            print ("TypeError: The seed is mandatory and cannot be a blank space.")
            exit ()
        if isinstance (O000OO0O0O0OO0000 ,(str ,int ,float ))!=True :
            OO000OOO0OO000OOO .data =O000OO0O0O0OO0000 
        else :
            OO000OOO0OO000OOO .data =bytes (str (O000OO0O0O0OO0000 ),'utf-8')
        if isinstance (OO000OOO0O0O0O0OO ,str )==True :
            OO000OOO0OO000OOO .seed =bytes (OO000OOO0O0O0O0OO ,'utf-8')
        else :
            OO000OOO0OO000OOO .seed =OO000OOO0O0O0O0OO 
        O0OOO0O0OOOO0OO0O =uuid .getnode ()
        OOO0OOOOOOOO0OO0O =base64 .encodebytes (bytes (str (O0OOO0O0OOOO0OO0O ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OO000OOO0OO000OOO .data +OOO0OOOOOOOO0OO0O +OO000OOO0OO000OOO .seed )
            hash128_2 =hashlib .shake_256 (OO000OOO0OO000OOO .data +OOO0OOOOOOOO0OO0O +OO000OOO0OO000OOO .seed )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2b (OO000OOO0OO000OOO .data +OO000OOO0OO000OOO .seed ,digest_size =34 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2b (OOO0OOOOOOOO0OO0O +OO000OOO0OO000OOO .seed ,digest_size =34 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2b (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =34 )
        O0OO0OO00OO00OO00 =hash128_1 .digest (14 )+hash128_2 .digest (16 )
        O00O0O0OO000OO00O =hash128_1 .hexdigest (14 )+hash128_2 .hexdigest (16 )
        OOOOOOOO0O0000OOO =O0OO0OO00OO00OO00 +UUIDHASH128_3 .digest ()
        O00O0O0OOO00O0O00 =O00O0O0OO000OO00O +UUIDHASH128_3 .hexdigest ()
        craxk_512_seedmutation .digest_size =len (OOOOOOOO0O0000OOO )
        craxk_512_seedmutation .block_size =len (O00O0O0OOO00O0O00 )
    def update (OOO0OO00O0000O00O ,OO00OOOO0O00O0OO0 =''):
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OO00OOOO0O00O0OO0 ,(str ,int ,float ))!=True :
            OOO0OO00O0000O00O .data =OOO0OO00O0000O00O .data +OO00OOOO0O00O0OO0 
        else :
            OOO0OO00O0000O00O .data =OOO0OO00O0000O00O .data +bytes (str (OO00OOOO0O00O0OO0 ),'utf-8')
        OOO0OO00O0000O00O .seed =OOO0OO00O0000O00O .seed 
        O00O000O0O0OO00O0 =uuid .getnode ()
        O0O000O0O0O000000 =base64 .encodebytes (bytes (str (O00O000O0O0OO00O0 ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (OOO0OO00O0000O00O .data +O0O000O0O0O000000 +OOO0OO00O0000O00O .seed )
            hash128_2 =hashlib .shake_256 (OOO0OO00O0000O00O .data +O0O000O0O0O000000 +OOO0OO00O0000O00O .seed )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2b (OOO0OO00O0000O00O .data +OOO0OO00O0000O00O .seed ,digest_size =34 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2b (O0O000O0O0O000000 +OOO0OO00O0000O00O .seed ,digest_size =34 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2b (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =34 )
        O0O0000OOO000000O =hash128_1 .digest (14 )+hash128_2 .digest (16 )
        O0000O00OOO0O00O0 =hash128_1 .hexdigest (14 )+hash128_2 .hexdigest (16 )
        O00OO00OOOOO0OO0O =O0O0000OOO000000O +UUIDHASH128_3 .digest ()
        OOO0OO0000OO0OO00 =O0000O00OOO0O00O0 +UUIDHASH128_3 .hexdigest ()
        craxk_512_seedmutation .digest_size =len (O00OO00OOOOO0OO0O )
        craxk_512_seedmutation .block_size =len (OOO0OO0000OO0OO00 )
    def replace (O0O0OOO0O0O0O00OO ,OO000O0OO00O0O0OO ='',OO00O00000O0OOOO0 =''):
        if OO00O00000O0OOOO0 =='':
            print ("ExceptCode 202")
            print ("TypeError: The seed is mandatory and cannot be a blank space.")
            exit ()
        global hash128_1 ,hash128_2 ,UUIDHASH128_1 ,UUIDHASH128_2 ,UUIDHASH128_3 
        if isinstance (OO000O0OO00O0O0OO ,(str ,int ,float ))!=True :
            O0O0OOO0O0O0O00OO .data =OO000O0OO00O0O0OO 
        else :
            O0O0OOO0O0O0O00OO .data =bytes (str (OO000O0OO00O0O0OO ),'utf-8')
        if isinstance (OO00O00000O0OOOO0 ,str )==True :
            OO00O00000O0OOOO0 =bytes (OO00O00000O0OOOO0 ,'utf-8')
        else :
            pass 
        O0OO0000OOOO0OOOO =uuid .getnode ()
        OOO0O0OOO00OOO000 =base64 .encodebytes (bytes (str (O0OO0000OOOO0OOOO ),'utf-8'))
        try :
            hash128_1 =hashlib .shake_128 (O0O0OOO0O0O0O00OO .data +OOO0O0OOO00OOO000 +OO00O00000O0OOOO0 )
            hash128_2 =hashlib .shake_256 (O0O0OOO0O0O0O00OO .data +OOO0O0OOO00OOO000 +OO00O00000O0OOOO0 )
        except TypeError :
            print ("ExceptCode 202")
            print ("TypeError: Unicode-objects must be encoded before hashing")
            exit ()
        UUIDHASH128_1 =hashlib .blake2s (O0O0OOO0O0O0O00OO .data +OO00O00000O0OOOO0 ,digest_size =3 ).hexdigest ()
        UUIDHASH128_2 =hashlib .blake2s (OOO0O0OOO00OOO000 +OO00O00000O0OOOO0 ,digest_size =2 ).hexdigest ()
        UUIDHASH128_3 =hashlib .blake2s (UUIDHASH128_1 .encode ('utf-8')+UUIDHASH128_2 .encode ('utf-8'),digest_size =5 )
        O00OOO0OOO0OO0000 =hash128_1 .digest (5 )+hash128_2 .digest (6 )
        OO0000OO000OO0O0O =hash128_1 .hexdigest (5 )+hash128_2 .hexdigest (6 )
        O00OOO0O00O0O000O =O00OOO0OOO0OO0000 +UUIDHASH128_3 .digest ()
        O0000OO0O00O0OOO0 =OO0000OO000OO0O0O +UUIDHASH128_3 .hexdigest ()
        craxk_512_seedmutation .digest_size =len (O00OOO0O00O0O000O )
        craxk_512_seedmutation .block_size =len (O0000OO0O00O0OOO0 )
    def hexdigest (O000O0OOO0O0OOO0O ):
        O00O0O00O00000O0O =hash128_1 .hexdigest (14 )+hash128_2 .hexdigest (16 )
        OO000000OO00O00OO =O00O0O00O00000O0O +UUIDHASH128_3 .hexdigest ()
        return OO000000OO00O00OO 
    def digest (OOO0O0000OOO0000O ):
        O0O0O0O000OOO0O0O =hash128_1 .digest (14 )+hash128_2 .digest (16 )
        OOOOOOOO00O00O00O =OOOOOOOO00O00O00O =O0O0O0O000OOO0O0O +UUIDHASH128_3 .digest ()
        return OOOOOOOO00O00O00O