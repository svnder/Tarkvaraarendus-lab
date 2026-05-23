"""
Abifunktsioonid kõigile patch skriptidele.
- run_rebuild() teeb docker compose rebuildi taustal
- wait_for_service() ootab kuni teenus vastab
"""
import subprocess
import time
import urllib.request
import urllib.error


def run_rebuild(compose_file):
    """Käivita docker compose rebuild taustal."""
    print("")
    print("🔨 Käivitan rebuildi taustal...")
    print("   (See võib võtta 10-30 sekundit)")
    print("")

    # Peata vanad konteinerid
    subprocess.run(
        ["docker", "compose", "-f", compose_file, "down"],
        capture_output=True
    )

    # Käivita uuesti taustal (--build = rebuild, -d = taustal)
    result = subprocess.run(
        ["docker", "compose", "-f", compose_file, "up", "--build", "-d"],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print("❌ Rebuild ebaõnnestus!")
        print(result.stderr)
        return False

    return True


def wait_for_service(url, max_seconds=30):
    """Oota kuni teenus on valmis vastama."""
    print(f"⏳ Ootan kuni teenus käivitub... ({url})")

    for i in range(max_seconds):
        try:
            urllib.request.urlopen(url, timeout=1)
            print(f"✅ Teenus on valmis! ({i+1} sekundit)")
            return True
        except (urllib.error.URLError, ConnectionResetError):
            time.sleep(1)

    print(f"⚠️  Teenus ei vastanud {max_seconds} sekundi jooksul")
    print("   Kontrolli logisid: docker logs epood-monolith")
    return False
