from telethon import events
from subprocess import Popen as SSSU, PIPE, STDOUT
from os import getcwd as CWD
from threading import Thread
from html import escape as FIX
from telethon import TelegramClient
from telethon.sessions import StringSession
from logging import INFO, basicConfig, getLogger

"""Logging"""
basicConfig(format="%(message)s", level=INFO)
LOGS = getLogger(__name__)

"""Account Vars"""
API_KEY = "20723503"
API_HASH = "85cd3ed85868ec1a56468172ddca4353"
STRING_SESSION = "1AZWarzwBuwKTqEtx4H9K7MVt9cmRiJWTepnTSZJf1_JILO385jjVd8S9Jorj1eSJDUeJ0tDnaeQYOoDo8JhRDszXa3Uwoqp7KVh8lL8WbcZIlPlzJ1JD3778CQ8dWWhL1Y-ZBcLeIaX3a0mBBCvI9UcSZWLeEBIxiR8qv8Ut1ndH1z8uoxi7R7PsQhqgZTHfGlU5EvBFigs1ntKLglswtIWrcNy4Czfl_LsOE0nHqgwwWRL-39tzp6MGWoTt34ot3yeTJdMefBRTBi5W_QEdGiqIYNouWYGzI9GMeGGZSUU0B4cNfHbWdq6eWYainAFTyZU3ZcgRE_N3_bPzILrbdjgGSTfcCPM="

"""Define & Start Client"""
bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
bot.start()

"""Lovely Vars"""
SHELL_PATH = '/data/data/com.termux/files/usr/bin/bash'
CORE = {
    'SUDO': 'sudo',
    'ISUDO': 'isudo',
    'DMUTE': 'dmute'
}
PENDING = {}

"""Spy For Triggers"""
def SPY(**a):
    p = a.get('p', None)
    if p: a['pattern'] = '(?i)' + p
    def d(f):
        async def w(c):
            try: await f(c)
            except KeyboardInterrupt: pass
        bot.add_event_handler(w, events.MessageEdited(**a))
        bot.add_event_handler(w, events.NewMessage(**a))
        return w
    return d

"""Triggers"""
SU_TRIG = r"\."
WHAT_TRIG = r"ID$"
DUMP_TRIG = r"DUMP THIS$"
ADD_SUDO_TRIG = r"TAKE SUDO$"
NUKE_SUDO_TRIG = r"NUKE SUDO$"
ADD_ISUDO_TRIG = r"TAKE ISUDO$"
NUKE_ISUDO_TRIG = r"NUKE ISUDO$"
ADD_DMUTE_TRIG = r"TAKE DMUTE$"
NUKE_DMUTE_TRIG = r"NUKE DMUTE$"
SUDO_YES_TRIG = r"y$"
NUKE_TRIG = r"n$"
UPLOAD_TRIG = r"PUSH"
DOWNLOAD_TRIG = r"PULL"
ABORT_TRIG = r"\^C"
HTML_TRIG = r"HTML THIS"

"""Strings"""
AFTER_DMUTE = "Now I may shut you up when I can, {}"
AFTER_DMUTE_NUKE = "I will stop trying to shut you up, {}"
AFTER_SUDO = "Now you have a protected access to my shell, {}"
AFTER_SUDO_NUKE = "You no longer have a protected access to my shell, {}"
AFTER_ISUDO = "Now you have full access to my shell, {}"
AFTER_ISUDO_NUKE = "You no longer have full access to my shell, {}"
NOT_THERE = "He's not there anyway"

"""Fix Missing Files"""
[open(CORE[f], 'a').close() for f in CORE]

"""Get, Edit, Inspect & Send Messages"""
async def GR(E,b=0): m = await E.get_reply_message(); return (m,T(m)) if b and m else m if m else (None,None)
async def ED(E,t):
    try: return await E.edit(t, parse_mode='HTML')
    except Exception as ex:
        if "not modified" in str(ex): pass
        else: return await SM(E.chat_id if hasattr(E, 'chat_id') else E.peer_id.channel_id, t)
async def SM(id,t): return await bot.send_message(id,t, parse_mode='HTML')
def T(E):
    return E.text if hasattr(E, 'text') else E.message.text

"""Obtain ID, User, Entity & Info"""
async def EN(id): return await bot.get_entity(int(id))
def U(EN,i=0): return EN.username if not i else (EN.username, EN.first_name)
def ID(E): return E.sender_id

"""Execute & Get SUDO"""
def SSU(C, **kw):
    return SSSU([SHELL_PATH, '-c', C], stdout=PIPE, stderr=STDOUT, text=True, **kw)
def SU(C):
    try: o = FIX(SSU(C).stdout.read())
    except Exception as e: o = F(FIX(0),'blockquote')+f"{e}"+F(None,'blockquote')
    if len(o)+len(C) >= 4000: o = f"{M(o[:4000-len(C)])}{F(0,'blockquote')}\n{Q(M('[CUT OUTPUT TO '+str(4000 - len(C))+'/'+str(len(o)+len(C))+' CHARS; NO MORE SPACE]'))}{F([],'blockquote')}"
    return Q(M('$ ')+M(C)+M('\n'+o if o else ''))
def GS(): return EYE('SUDO')
def GIS(): return EYE('ISUDO')
def GDM(): return EYE('DMUTE')

"""Markdown"""
def F(t,u): return f"<{u}>{t}</{u}>" if t else f"</{u}><{u}>" if t == 0 else f"</{u}>"
def Q(t): return F(t,'blockquote')
def M(t): return F(t,'code')
def P(t): return F(t,'pre')

"""Read, Write & Append"""
def PIN(n,t):
    with open(CORE[n],'w') as f: f.write(t)
def PEN(n,t):
    with open(CORE[n],'a') as f: f.write(t)
def EYE(n):
    with open(CORE[n]) as f: return f.read().strip().split('\n')

"""Message Dump"""
@SPY(pattern=DUMP_TRIG)
async def dump(E):
    await ED(E, Q(P(str((await GR(E)) if E.is_reply else E))))

"""ID Identifier"""
@SPY(pattern=WHAT_TRIG)
async def what(E):
    id = ID(E if not E.is_reply else await GR(E))
    if E.is_reply: await ED(E, Q(M(id)))
    else: await E.reply(Q(M(id)), parse_mode='HTML')

"""Add SUDO"""
@SPY(outgoing=True, pattern=ADD_SUDO_TRIG)
async def add_sudo(E):
    if not E.is_reply: return
    id = ID(await GR(E))
    PEN('SUDO', '\n'+str(id))
    await ED(E, Q(M(AFTER_SUDO.format(U(await EN(id))))))

"""Nuke SUDO"""
@SPY(outgoing=True, pattern=NUKE_SUDO_TRIG)
async def nuke_sudo(E):
    if not E.is_reply: return
    id = ID(await GR(E))
    if str(id) not in GS(): await ED(E, Q(M(NOT_THERE))); return
    old = GS()
    new = [l for l in old if str(id) not in l]
    PIN('SUDO', '\n'.join(new))
    await ED(E, Q(M(AFTER_SUDO_NUKE.format(U(await EN(id))))))

"""Nuke ISUDO"""
@SPY(outgoing=True, pattern=NUKE_ISUDO_TRIG)
async def nuke_isudo(E):
    if not E.is_reply: return
    id = ID(await GR(E))
    if str(id) not in GIS(): await ED(E, Q(M(NOT_THERE))); return
    old = GIS()
    new = [l for l in old if str(id) not in l]
    PIN('ISUDO', '\n'.join(new))
    await ED(E, Q(M(AFTER_ISUDO_NUKE.format(U(await EN(id))))))

"""Add ISUDO"""
@SPY(outgoing=True, pattern=ADD_ISUDO_TRIG)
async def add_isudo(E):
    if not E.is_reply: return
    id = ID(await GR(E))
    PEN('ISUDO', '\n'+str(id))
    await ED(E, Q(M(AFTER_ISUDO.format(U(await EN(id))))))

"""Add Dmute"""
@SPY(outgoing=True, pattern=ADD_DMUTE_TRIG)
async def add_dmute(E):
    if not E.is_reply: return
    id = ID(await GR(E))
    PEN('DMUTE', '\n'+str(id))
    await ED(E, Q(M(AFTER_DMUTE.format(U(await EN(id))))))

"""Nuke Dmute"""
@SPY(outgoing=True, pattern=NUKE_DMUTE_TRIG)
async def nuke_dmute(E):
    if not E.is_reply: return
    id = ID(await GR(E))
    if str(id) not in GDM(): await ED(E, Q(M(NOT_THERE))); return
    old = GDM()
    new = [l for l in old if str(id) not in l]
    PIN('DMUTE', '\n'.join(new))
    await ED(E, Q(M(AFTER_DMUTE_NUKE.format(U(await EN(id))))))

"""Abort Shell Commands"""
@SPY(outgoing=True, pattern=ABORT_TRIG)
async def abort_shell(E):
    if not E.is_reply: return
    r = await GR(E)
    PENDING[str(r)[:20]].kill()
    await E.delete()

"""HTML Markdown Tester"""
@SPY(pattern=HTML_TRIG)
async def html(E):
    if not E.is_reply: return
    t = T(await GR(E))
    try: await E.delete()
    except: pass
    await ED(E,t)

"""Live Shell Command Listener"""
@SPY(outgoing=True, pattern=SU_TRIG)
async def shell(E):
    t = T(E)[1:]
    if "#LC=" in t: fn2 = int(t.split('#LC=',1)[1])
    else: fn2 = 0
    if fn2 == 0:
        outt = SU(t)
        await ED(E, outt)
        return
    else:
        if fn2 == 0:
            await ED(E, SU(t))
            return
        p = SSU(t)
        o = '\n'
        koll = p.kill
        def kell(*a,**kw):
            nonlocal koll, o
            o += "^C"
            koll(*a,**kw)
        p.kill = kell
        PENDING[str(E.message)[:20]] = p
        fn = 0
        async def a():
            nonlocal p, t, o, fn
            for l in p.stdout:
                if not l: continue
                o += l
                if fn % fn2 == 0: await ED(E,Q(M('$ ')+M(t)+M(o)))
                fn += 1
            await ED(E,Q(M('$ ')+M(t)+M(o)))
        th = Thread(target=(await a()))
        th.start()

"""SUDO Shell Command Listener"""
@SPY(pattern=SU_TRIG)
async def sub_shell(E):
    t = T(E)
    id = str(ID(E))
    if (id not in GS() and id not in GIS()): return
    cmd = t[1:]
    uname, fname = U(await EN(id),1)
    if id in GIS(): await ED(E, SU(t[1:]))
    else:
        final = Q(M('SHELL REQUEST - By\n')+M(f'{fname}')+' ('+M(f'@{uname}')+M(')'))
        final += "\n"+Q(M('# '+cmd))
        final += "\n"+Q(M('Waiting for confirmation'))
        msg = await SM(E.chat_id, final)

"""SUDO Pending Requests"""
@SPY(outgoing=True, pattern=SUDO_YES_TRIG)
async def sudo_yes(E):
    if not E.is_reply: return
    r, rt = await GR(E,1)
    try: t = rt.split('\n')[2][3:][:-1]
    except IndexError: return
    await ED(r, SU(t))
    await E.delete()

"""Delete A Message"""
@SPY(outgoing=True, pattern=NUKE_TRIG)
async def nuke(E):
    try:
        await E.delete()
        await (await GR(E)).delete()
    except: pass

"""Upload Files"""
@SPY(outgoing=True, pattern=UPLOAD_TRIG)
async def upload(E):
    t = T(E)
    if not t.startswith(UPLOAD_TRIG): return
    t = t[len(UPLOAD_TRIG)+1:]
    f = t if t.startswith('/') else CWD() + f'/{t}'
    async def CB(c,t):
        nonlocal E, f
        p = (c / t) * 100
        art = ""
        for i in range(20):
            art += "■" if i*5 < p else "□"
        c = str(c / 1024 / 1024)[:6]
        t = str(t / 1024 / 1024)[:6]
        p = str(p)[:6]
        pro = f"[{c}MB/{t}MB]"
        await ED(E, Q(M(f'{UPLOAD_TRIG} ')+M(f)+M(f'\n{pro} {p}%\n')+M(art)))
    try: await bot.send_file(E.chat_id, f, progress_callback=CB)
    except Exception as e: await ED(E, Q(M(str(e))))

"""Upload Files"""
@SPY(outgoing=True, pattern=DOWNLOAD_TRIG)
async def download(E):
    t = T(E)
    if not t.startswith(DOWNLOAD_TRIG): return
    if not E.is_reply: return
    r = await GR(E)
    if not r.media: return
    t = t[len(DOWNLOAD_TRIG)+1:]
    f = t if t.startswith('/') else CWD() + f'/{t}'
    async def CB(c,t):
        nonlocal E, f
        p = (c / t) * 100
        art = ""
        for i in range(20):
            art += "■" if i*5 < p else "□"
        c = str(c / 1024 / 1024)[:6]
        t = str(t / 1024 / 1024)[:6]
        p = str(p)[:6]
        pro = f"[{c}MB/{t}MB]"
        await ED(E, Q(M(f'{DOWNLOAD_TRIG} ')+M(f)+M(f'\n{pro} {p}%\n')+M(art)))
    try: await r.download_media(f, progress_callback=CB)
    except Exception as e: await ED(E, Q(M(str(e))))

"""Event Listener"""
@bot.on(events.NewMessage)
async def ear(E):
    """Dmute"""
    if str(ID(E)) in GDM():
        try: await E.delete()
        except: pass

"""Keep Bot Alive"""
print ("BOT ON!")
bot.run_until_disconnected()
print ("BOT OFF!")
