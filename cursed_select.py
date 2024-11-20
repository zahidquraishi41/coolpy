import curses
import curses.ascii


def select(stdscr, items: list):

    def _draw(start_row, selected_row):
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        for idx, row in enumerate(items[start_row:start_row + h]):
            x = 0  # Start from the left
            y = idx  # Increment by 1 to move down
            if idx + start_row == selected_row:
                stdscr.addstr(y, x, row, curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        stdscr.refresh()


    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    stdscr.clear()
    stdscr.refresh()

    current_row = 0
    start_row = 0

    while True:
        _draw(start_row, current_row)

        key = stdscr.getch()
        if key == curses.ascii.ESC:
            break

        elif key == curses.KEY_RESIZE:
            h, w = stdscr.getmaxyx()
            if current_row >= start_row + h:
                start_row = current_row - h + 1

        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
            if current_row < start_row:
                start_row -= 1  # Scroll up

        elif key == curses.KEY_DOWN and current_row < len(items) - 1:
            h, w = stdscr.getmaxyx()
            current_row += 1
            if current_row >= start_row + h:
                start_row += 1  # Scroll down

        elif key == curses.KEY_ENTER or key in [10, 13]:
            return current_row

if __name__ == "__main__":
    files = ['appcompat', 'apppatch', 'AppReadiness', 'assembly', 'bcastdvr', 'bfsvc.exe', 'BitLockerDiscoveryVolumeContents', 'Boot', 'bootstat.dat', 'Branding', 'BrowserCore', 'CbsTemp', 'Containers', 'CSC', 'Cursors', 'debug', 'diagnostics', 'DiagTrack', 'DigitalLocker', 'Downloaded Program Files', 'DtcInstall.log', 'ELAMBKUP', 'en-US', 'explorer.exe', 'Fonts', 'GameBarPresenceWriter', 'Globalization', 'Help', 'HelpPaneX.exe', 'hh.exe', 'IdentityCRL', 'IME', 'ImmersiveControlPanel', 'InboxApps', 'INF', 'InputMethod', 'Installer', 'L2Schemas', 'LanguageOverlayCache', 'LiveKernelReports', 'Logs', 'lsasetup.log', 'Media', 'mib.bin', 'Microsoft.NET', 'Migration', 'ModemLogs', 'notepad.exe', 'NvContainerRecovery.bat', 'OCR', 'Offline Web Pages', 'Panther', 'Performance', 'PFRO.log', 'PLA', 'PolicyDefinitions', 'Prefetch', 'PrintDialog', 'Professional.xml', 'Provisioning', 'py.exe', 'pyshellext.amd64.dll', 'pyw.exe', 'regedit.exe', 'Registration', 'RemotePackages', 'rescache', 'Resources', 'SchCache', 'schemas', 'security', 'ServiceProfiles', 'ServiceState', 'servicing', 'Setup', 'setupact.log', 'setuperr.log', 'ShellComponents', 'ShellExperiences', 'SKB', 'SoftwareDistribution', 'Speech', 'Speech_OneCore', 'splwow64.exe', 'System', 'system.ini', 'System32', 'SystemApps', 'SystemResources', 'SystemTemp', 'SysWOW64', 'TAPI', 'Tasks', 'Temp', 'tracing', 'twain_32', 'twain_32.dll', 'UUS', 'Vss', 'WaaS', 'Web', 'win.ini', 'WindowsShell.Manifest', 'WindowsUpdate.log', 'winhlp32.exe', 'WinSxS', 'WMSysPr9.prx', 'write.exe', 'WUModels']
    curses.wrapper(select, files)

