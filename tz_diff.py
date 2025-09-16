# Create a single ready-to-run Python script for timezone conversion and offset difference.
from textwrap import dedent
import os, stat

path = "/mnt/data/tz_diff.py"
code = dedent("""
    #!/usr/bin/env python3
    \"\"\"
    tz_diff.py — Convert between time zones and show the offset difference.
    
    Usage:
      # Now, between New York and India (IST)
      python3 tz_diff.py --from now --src America/New_York --dst Asia/Kolkata
      
      # A specific time interpreted in the source TZ
      python3 tz_diff.py --from "2025-08-17 10:00" --src America/New_York --dst Asia/Kolkata
      
      # Only offsets (what's the DST-aware time difference right now?)
      python3 tz_diff.py --src Europe/London --dst Asia/Kolkata
    \"\"\"
    from __future__ import annotations
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    import argparse, sys
    
    def fmt_dt(dt: datetime) -> str:
        # 2025-08-17 10:00:00 (UTC-04:00)
        off = dt.utcoffset() or timedelta(0)
        sign = "+" if off >= timedelta(0) else "-"
        off_abs = abs(off)
        hh = off_abs.seconds // 3600 + off_abs.days * 24
        mm = (off_abs.seconds % 3600) // 60
        return f"{dt.strftime('%Y-%m-%d %H:%M:%S')} (UTC{sign}{hh:02d}:{mm:02d})"
    
    def parse_when(s: str | None, src_tz: ZoneInfo) -> datetime:
        if not s or s.lower() == "now":
            return datetime.now(src_tz)
        txt = s.strip().replace("T", " ")
        try:
            # Accept: YYYY-MM-DD, YYYY-MM-DD HH:MM, YYYY-MM-DD HH:MM:SS
            parts = txt.split()
            if len(parts) == 1:
                # date only
                dt = datetime.fromisoformat(parts[0])
            else:
                dt = datetime.fromisoformat(parts[0] + " " + parts[1])
        except Exception as e:
            raise SystemExit(f"Could not parse --from '{s}'. Try 'now' or 'YYYY-MM-DD HH:MM'. Error: {e}")
        # If the parsed datetime is naive, attach src timezone
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=src_tz)
        else:
            # ensure it's *interpreted* as provided (rare if user gave offset)
            dt = dt.astimezone(src_tz)
        return dt
    
    def main():
        ap = argparse.ArgumentParser(description="Timezone convert + DST-aware offset difference")
        ap.add_argument("--from", dest="when", default="now", help="Datetime like 'YYYY-MM-DD HH:MM' or 'now' (default)")
        ap.add_argument("--src", default="UTC", help="Source timezone (IANA name, default: UTC)")
        ap.add_argument("--dst", default="Asia/Kolkata", help="Destination timezone (default: Asia/Kolkata)")
        args = ap.parse_args()
    
        try:
            src = ZoneInfo(args.src)
        except Exception:
            raise SystemExit(f"Unknown source timezone: {args.src}. Try e.g. 'America/New_York', 'Europe/London'.")
        try:
            dst = ZoneInfo(args.dst)
        except Exception:
            raise SystemExit(f"Unknown destination timezone: {args.dst}.")
    
        dt_src = parse_when(args.when, src)
        dt_dst = dt_src.astimezone(dst)
    
        off_src = dt_src.utcoffset() or timedelta(0)
        off_dst = dt_dst.utcoffset() or timedelta(0)
        delta = off_dst - off_src
    
        # human delta string
        sign = "+" if delta >= timedelta(0) else "-"
        dabs = abs(delta)
        hours = dabs.seconds // 3600 + dabs.days * 24
        minutes = (dabs.seconds % 3600) // 60
    
        print("Source timezone :", args.src)
        print("Destination TZ  :", args.dst)
        print("Time in source  :", fmt_dt(dt_src))
        print("Time in dest    :", fmt_dt(dt_dst))
        print(f"Offset difference: {sign}{hours}h{minutes:02d}m "
              f"(i.e., '{args.dst}' is {('ahead of' if delta>timedelta(0) else 'behind')} '{args.src}' at this time)")
    
    if __name__ == "__main__":
        main()
""")
with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(code)
st = os.stat(path)
os.chmod(path, st.st_mode | stat.S_IEXEC)

path
