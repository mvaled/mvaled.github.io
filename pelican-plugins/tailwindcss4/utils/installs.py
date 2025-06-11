from .commands import run_in_plugin


def plugins(settings, cwd):
    plugins = settings.get("plugins", None)

    # In the list of plugins, there may also be other NodeJS packages.
    # Here we make sure that we only have Tailwind plugins in the list.
    only_tw_plugins = [x for x in plugins if "@tailwindcss/" in x]

    if only_tw_plugins and len(only_tw_plugins):
        run_in_plugin(f"npm i {' '.join(only_tw_plugins)}", cwd=cwd)
