import cloudscraper
import asyncio
import random
import aiohttp
from colorama import *
import json
import os
import sys
import time
from datetime import datetime
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError, Timeout, ProxyError, RequestException, HTTPError

init(autoreset=True)

# Colors
mrh = Fore.LIGHTRED_EX
pth = Fore.LIGHTWHITE_EX
hju = Fore.LIGHTGREEN_EX
kng = Fore.LIGHTYELLOW_EX
bru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
htm = Fore.LIGHTBLACK_EX

last_log_message = None

# Functions from key.py
async def loading_animation(message, duration):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        try:
            print(f"\r{frames[i % len(frames)]} {message}", end="", flush=True)
        except UnicodeEncodeError:
            print(f"\r* {message}", end="", flush=True)
        i += 1
        await asyncio.sleep(0.1)
    print("\r" + " " * (len(message) + 2) + "\r", end="", flush=True)

def log_message(message, color=Fore.RESET, status="", end='\n'):
    status_symbol = "[+] ║" if status == "success" else "[-] ║" if status == "fail" else "[*] ║"
    sys.stdout.write(f"{color}{status_symbol} {message}{Fore.RESET}{end}")
    sys.stdout.flush()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(f"""{Fore.BLUE}
╔═══════════════════════════════════════════╗
║              Bot Automation               ║
║         Developed by @ItbaArts_Dev        ║
╚═══════════════════════════════════════════╝{Style.RESET_ALL}""")

def read_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as file:
        try:
            config_content = file.read()
            return json.loads(config_content)
        except json.JSONDecodeError as e:
            return {}

def log_error(message):
    log_message(f"ERROR - {message}", color=Fore.LIGHTRED_EX, status="fail")

async def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"{pth}please wait until {h}:{m}:{s} ", flush=True, end="\r")
        seconds -= 1
        await asyncio.sleep(1)
    print(f"{pth}please wait until {h}:{m}:{s} ", flush=True, end="\r")

# Functions from agent.py
def generate_random_user_agent(device_type='android', browser_type='chrome'):
    chrome_versions = list(range(110, 127))
    firefox_versions = list(range(90, 100))
    safari_versions = list(range(14, 16))
    edge_versions = list(range(90, 100))

    if browser_type == 'chrome':
        major_version = random.choice(chrome_versions)
        minor_version = random.randint(0, 9)
        build_version = random.randint(1000, 9999)
        patch_version = random.randint(0, 99)
        browser_version = f"{major_version}.{minor_version}.{build_version}.{patch_version}"
    elif browser_type == 'firefox':
        browser_version = random.choice(firefox_versions)
    elif browser_type == 'safari':
        major_version = random.choice(safari_versions)
        minor_version = random.randint(0, 9)
        browser_version = f"{major_version}.{minor_version}"
    elif browser_type == 'edge':
        major_version = random.choice(edge_versions)
        minor_version = random.randint(0, 9)
        build_version = random.randint(1000, 9999)
        patch_version = random.randint(0, 99)
        browser_version = f"{major_version}.{minor_version}.{build_version}.{patch_version}"

    if device_type == 'android':
        android_versions = ['10.0', '11.0', '12.0', '13.0']
        android_device = random.choice([
            'SM-G960F', 'Pixel 5', 'SM-A505F', 'Pixel 4a', 'Pixel 6 Pro', 'SM-N975F',
            'SM-G973F', 'Pixel 3', 'SM-G980F', 'Pixel 5a', 'SM-G998B', 'Pixel 4',
            'SM-G991B', 'SM-G996B', 'SM-F711B', 'SM-F916B', 'SM-G781B', 'SM-N986B',
            'SM-N981B', 'Pixel 2', 'Pixel 2 XL', 'Pixel 3 XL', 'Pixel 4 XL',
            'Pixel 5 XL', 'Pixel 6', 'Pixel 6 XL', 'Pixel 6a', 'Pixel 7', 'Pixel 7 Pro',
            'OnePlus 8', 'OnePlus 8 Pro', 'OnePlus 9', 'OnePlus 9 Pro', 'OnePlus Nord', 'OnePlus Nord 2',
            'OnePlus Nord CE', 'OnePlus 10', 'OnePlus 10 Pro', 'OnePlus 10T', 'OnePlus 10T Pro',
            'Xiaomi Mi 9', 'Xiaomi Mi 10', 'Xiaomi Mi 11', 'Xiaomi Redmi Note 8', 'Xiaomi Redmi Note 9',
            'Huawei P30', 'Huawei P40', 'Huawei Mate 30', 'Huawei Mate 40', 'Sony Xperia 1',
            'Sony Xperia 5', 'LG G8', 'LG V50', 'LG V60', 'Nokia 8.3', 'Nokia 9 PureView'
        ])
        android_version = random.choice(android_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Linux; Android {android_version}; {android_device}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Android {android_version}; Mobile; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")
        elif browser_type == 'safari':
            return (f"Mozilla/5.0 (Linux; Android {android_version}; {android_device}) AppleWebKit/605.1.15 "
                    f"(KHTML, like Gecko) Version/{browser_version} Mobile/15E148 Safari/604.1")
        elif browser_type == 'edge':
            return (f"Mozilla/5.0 (Linux; Android {android_version}; {android_device}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36 EdgA/{browser_version}")

    elif device_type == 'ios':
        ios_versions = ['13.0', '14.0', '15.0', '16.0']
        ios_version = random.choice(ios_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/537.36 (KHTML, like Gecko) CriOS/{browser_version} Mobile/15E148 Safari/604.1")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{browser_version}.0 Mobile/15E148 Safari/605.1.15")
        elif browser_type == 'safari':
            return (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{browser_version} Mobile/15E148 Safari/604.1")
        elif browser_type == 'edge':
            return (f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/537.36 (KHTML, like Gecko) Version/{browser_version} Mobile/15E148 Safari/604.1 EdgiOS/{browser_version}")

    elif device_type == 'windows':
        windows_versions = ['10.0', '11.0']
        windows_version = random.choice(windows_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")
        elif browser_type == 'safari':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    f"Version/{browser_version} Safari/537.36")
        elif browser_type == 'edge':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36 Edg/{browser_version}")

    elif device_type == 'ubuntu':
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{browser_version}.0) Gecko/{browser_version}.0 "
                    f"Firefox/{browser_version}.0")
        elif browser_type == 'safari':
            return (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{browser_version}.0) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    f"Version/{browser_version} Safari/537.36")
        elif browser_type == 'edge':
            return (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{browser_version}.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36 Edg/{browser_version}")

    return None

# Functions from headers.py
def get_headers(acc_data):
    platforms = ['"Windows"', '"Linux"', '"macOS"']

    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Init-Data": acc_data,
        "Origin": "https://tonclayton.fun",
        "Priority": "u=1, i",
        "Referer": "https://tonclayton.fun/games/game-stack",
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": random.choice(platforms),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": generate_random_user_agent(),
    }

# Classes and functions from core.py
cfg = read_config()

class GameSession:
    def __init__(self, acc_data, tgt_score, prxy=None):
        self.b_url = "https://tonclayton.fun"
        self.s_id = None
        self.a_data = acc_data
        self.hdrs = get_headers(self.a_data)
        self.c_score = 0
        self.t_score = tgt_score
        self.inc = 10
        self.pxy = prxy

        self.scraper = cloudscraper.create_scraper()  
        if self.pxy:
            self.scraper.proxies = {
                'http': f'http://{self.pxy}',
                'https': f'http://{self.pxy}',
            }

    @staticmethod
    def fmt_ts(ts):
        dt = datetime.fromisoformat(ts[:-1])
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def proxy_format(proxy):
        if proxy:
            return proxy.split('@')[-1]
        return 'No proxy used'

    async def start(self):
        lg_url = f"{self.b_url}/api/user/authorization"
        while True:
            await loading_animation("Starting session", 2)
            resp = self.scraper.post(lg_url, headers=self.hdrs, json={})
            if resp.status_code == 200:
                usr_data = resp.json()
                usr = usr_data.get('user', {})
                log_message(f"Proxy: {self.proxy_format(self.pxy)}", color=hju)
                log_message("═" * 38, color=htm)
                log_message(f"Username: {usr.get('username', 'N/A')}", color=bru)
                log_message(f"Points: {usr.get('tokens', 'N/A'):,.0f} | XP: {usr.get('current_xp', 'N/A')}", color=hju)
                log_message(f"Level: {usr.get('level', 'N/A')} | Tickets: {usr.get('daily_attempts', 0)}", color=hju)
                await self.check_in()
                break  
            else:
                await loading_animation("Retrying", 2)
                await asyncio.sleep(2) 
  
    async def check_in(self):
        await loading_animation("Performing daily check-in", 2)
        lg_url = f"{self.b_url}/api/user/daily-claim"
        resp = self.scraper.post(lg_url, headers=self.hdrs, json={})
        if resp.status_code == 200:
            res = resp.json()
            daily_attempts = res.get('daily_attempts', 0)
            consecutive_days = res.get('consecutive_days', 0)
            log_message("Successfully claimed daily check-in", color=hju)
            log_message(f"Daily Attempts: {daily_attempts} | Consecutive Days: {consecutive_days}", color=hju)
        elif resp.status_code == 400:
            log_message("You have already checked in today!", color=kng)
        else:
            log_message("Failed to retrieve check-in data!", color=bru)

        await asyncio.sleep(2)

    async def run_g(self):
        with open('config.json') as cf:
            g_tickets = json.load(cf).get("game_ticket_to_play", 1)

        for ticket in range(g_tickets):
            game_choice = random.choice(['clayball', 'stack', 'tiles'])
            await loading_animation(f"Playing {game_choice}", 2)
            log_message(f"Playing {game_choice} with ticket {ticket + 1}/{g_tickets}", color=hju)

            if game_choice == 'stack':
                if not await self.play_stack_game():
                    break
                
            elif game_choice == 'tiles':
                if not await self.play_tiles_game():
                    break
            
            elif game_choice == 'clayball':
                if not await self.play_clay_ball():
                    break

            await countdown_timer(5)

    async def play_stack_game(self):
        if not await self.start_game(f"{self.b_url}/api/stack/st-game"):
            return False

        self.c_score = 0
        while self.c_score < self.t_score:
            self.c_score += self.inc
            await self.update_score(f"{self.b_url}/api/stack/update-game", {"score": self.c_score})

        return await self.end_game(f"{self.b_url}/api/stack/en-game", {"score": self.c_score, "multiplier": 1})

    async def play_tiles_game(self):
        if not await self.start_game(f"{self.b_url}/api/game/start"):
            return False

        max_tile = 2
        updates = random.randint(7, 10)

        for _ in range(updates):
            await self.update_score(f"{self.b_url}/api/game/save-tile", {"maxTile": max_tile})
            max_tile *= 2

        return await self.end_game(f"{self.b_url}/api/game/over", {"multiplier": 1})

    async def start_game(self, url):
        await loading_animation("Starting game", 2)
        resp = self.scraper.post(url, headers=self.hdrs, json={})
        if resp.status_code != 200:
            if "attempts are over" in resp.text:
                error_msg = kng + "Game: ticket attempts are over"
                log_message(error_msg)
            return False
        log_message("Game started successfully", color=bru)
        return True

    async def update_score(self, url, payload):
        await loading_animation("Updating score", 1)
        resp = self.scraper.post(url, headers=self.hdrs, json=payload)

        if resp.status_code == 200:
            score_type = 'maxTile' if 'maxTile' in payload else 'score'
            log_message(f"New score: [ {payload[score_type]} ]", color=hju, end="\r")

        await asyncio.sleep(random.randint(2, 5))

    async def end_game(self, url, payload):
        await loading_animation("Ending game", 2)
        resp = self.scraper.post(url, headers=self.hdrs, json=payload)

        if resp.status_code == 200:
            res = resp.json()
            log_message("Game ended successfully", color=hju)
            log_message(f"XP Earned: {res['xp_earned']} | Points: {res['earn']}", color=hju)

        await countdown_timer(5)
        return True

    async def play_clay_ball(self):
        if not await self.starts_game("https://tonclayton.fun/api/clay/start-game"):
            return False
        await countdown_timer(10)

        cl_score = random.randint(40,45)
        payload = {"score": cl_score}
        return await self.ends_game("https://tonclayton.fun/api/clay/end-game", payload)

    async def starts_game(self, url):
        resp = self.scraper.post(url, headers=self.hdrs, json={})

        if resp.status_code != 200:
            if "attempts are over" in resp.text:
                error_msg = kng + "Game: ticket attempts are over"
                log_message(error_msg)
            return False

        log_message("Game started successfully", color=bru)
        return True

    async def ends_game(self, url, payload):
        resp = self.scraper.post(url, headers=self.hdrs, json=payload)

        if resp.status_code == 200:
            res = resp.json()
            log_message("Game ended successfully", color=hju)
            log_message(f"CL: {res['cl']} | Multiplier: {res['multiplier']} | Reward: {res['reward']}", color=hju)

        await countdown_timer(5)
        return True
        
    async def cpl_and_clm_tsk(self, tsk_type='daily'):
        if tsk_type == 'daily':
            t_url = f"{self.b_url}/api/tasks/daily-tasks"
        elif tsk_type == 'default':
            t_url = f"{self.b_url}/api/tasks/default-tasks"
        elif tsk_type == 'super':
            t_url = f"{self.b_url}/api/tasks/super-tasks"
        elif tsk_type == 'partner':
            t_url = f"{self.b_url}/api/tasks/partner-tasks"
        else:
            log_message(f"Unknown task type: {tsk_type}", color=mrh)
            return

        await countdown_timer(random.randint(3, 4))
        
        tasks = [] 
        for attempt in range(3):
            resp = self.scraper.get(t_url, headers=self.hdrs)
            if resp.status_code == 200:
                if not resp.text:
                    log_message("Received empty response from the server.", color=mrh)
                    return
                tasks = resp.json()
                break 

            else:
                log_message(f"Failed to decode {tsk_type} [{attempt + 1}]", color=kng)
                await asyncio.sleep(3)
                if attempt == 2:
                    return 

        for t in tasks:
            t_id = t['task_id']
            if not t.get('is_completed', False):
                cmp_url = f"{self.b_url}/api/tasks/complete"
                cmp_resp = self.scraper.post(cmp_url, headers=self.hdrs, json={"task_id": t_id})
                if cmp_resp.status_code == 200:
                    log_message(f"Completed {tsk_type} task: {t['task']['title']}", color=hju)
                    wait_time = max(random.randint(4, 6), 1)
                    await countdown_timer(wait_time)
                    clm_url = f"{self.b_url}/api/tasks/claim"
                    clm_resp = self.scraper.post(clm_url, headers=self.hdrs, json={"task_id": t_id})
                    if clm_resp.status_code == 200:
                        clm_data = clm_resp.json()
                        log_message(f"Claimed {t['task']['title']} | Reward: {clm_data.get('reward_tokens', '0')}", color=hju)
                    else:
                        error_message = clm_resp.json().get('error', 'Unknown error')
                        log_message(f"Failed to claim {t_id}: {error_message}", color=mrh)
                else:
                    error_message = cmp_resp.json().get('error', 'Unknown error')
                    log_message(f"Failed! Task {t_id}: {error_message}", color=mrh)
            else:
                log_message(f"Task {t['task']['title']} already completed.", color=hju)

    async def claim_achievements(self):
        ach_url = f"{self.b_url}/api/user/achievements/get"
        resp = self.scraper.post(ach_url, headers=self.hdrs, json={})
        if resp.status_code != 200:
            return

        achievements = resp.json()
        claimed_any = False  

        for category in ['friends', 'games', 'stars']:
            for achievement in achievements[category]:
                if achievement['is_completed'] and not achievement['is_rewarded']:
                    lvl = achievement['level']
                    pl = {"type": category, "level": lvl}
                    cl_url = f"{self.b_url}/api/user/achievements/claim"
                    claim_resp = self.scraper.post(cl_url, headers=self.hdrs, json=pl)
                    if claim_resp.status_code == 200:
                        rwd_data = claim_resp.json()
                        log_message(f"Achievement {category} level {lvl}: Reward {rwd_data['reward']}", color=hju)
                        claimed_any = True 
                    else:
                        log_message(f"Can't claim {category} achievement lvl {lvl}", color=kng)

        if not claimed_any:
            log_message("No achievements reward to claim", color=kng)

async def ld_accs(fp):
    with open(fp, 'r') as file:
        return [line.strip() for line in file.readlines()]

async def ld_prx(fp):
    with open(fp, 'r') as file:
        return [line.strip() for line in file.readlines()]

async def main():
    tgt_score = random.randint(45, 59)
    use_prxy = cfg.get('use_proxy', False)
    ply_game = cfg.get('play_game', False)
    cpl_tsk = cfg.get('complete_task', False)
    acc_dly = cfg.get('account_delay', 5)
    cntdwn_loop = cfg.get('countdown_loop', 3800)
    prx = await ld_prx('proxies.txt') if use_prxy else []
    accs = await ld_accs("data.txt")

    while True:
        try:
            async with aiohttp.ClientSession():
                for idx, acc in enumerate(accs):
                    await loading_animation(f"Processing account {idx + 1} of {len(accs)}", 2)
                    log_message(f"Processing account {idx + 1} of {len(accs)}", color=hju)
                    prxy = prx[idx % len(prx)] if use_prxy and prx else None
                    game = GameSession(acc, tgt_score, prxy)

                    await game.start()

                    if cpl_tsk:
                        await loading_animation("Completing tasks", 2)
                        await game.cpl_and_clm_tsk(tsk_type='daily')
                        await game.cpl_and_clm_tsk(tsk_type='partner')
                        await game.cpl_and_clm_tsk(tsk_type='default')
                        await game.cpl_and_clm_tsk(tsk_type='super')

                    if ply_game:
                        await loading_animation("Playing game", 2)
                        await game.run_g()

                    await countdown_timer(3)    
                    await loading_animation("Claiming achievements", 2)
                    await game.claim_achievements()

                    log_message("═" * 60, color=pth)
                    await countdown_timer(acc_dly)
                await loading_animation("Waiting for the next round", 5)
                await countdown_timer(cntdwn_loop)

        except HTTPError as e:
            log_message(f"HTTP error occurred, check last.log for details", color=mrh)
            log_error(f"{str(e)}")
            continue
        except (IndexError, JSONDecodeError) as e:
            log_message(f"Data extraction error: check last.log for details.", color=mrh)
            log_error(f"{str(e)}")
            continue
        except ConnectionError:
            log_message(f"Connection lost: Unable to reach the server.", color=mrh)
            continue
        except Timeout:
            log_message(f"Request timed out: The server is taking too long to respond.", color=mrh)
            continue
        except ProxyError as e:
            log_message(f"Proxy error: Failed to connect through the specified proxy.", color=mrh)
            log_error(f"{str(e)}")
            if "407" in str(e):
                log_message(f"Proxy authentication failed. Trying another.", color=bru)
                if prx:
                    proxy = random.choice(prxy)
                    log_message(f"Switching proxy: {proxy}", color=bru)
                else:
                    log_message(f"No more proxies available.", color=mrh)
                    break
            else:
                log_message(f"An error occurred: {e}", color=htm)
                break
            continue
        except ValueError as e:
            log_message(f"Received non-JSON response, check last.log", color=mrh)
            log_error(f"{str(e)}")
            continue
        except RequestException as e:
            log_message(f"An error occurred, check last.log", color=mrh)
            log_error(f"{str(e)}")
            return

if __name__ == "__main__":
    clear_terminal()
    print_header()
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            log_message(f"Stopping due to keyboard interrupt.", color=mrh)
            sys.exit()