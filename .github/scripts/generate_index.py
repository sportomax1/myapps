import os
import sys
import json

def generate_index_html(target_directory="localonly"):
    """
    Scans the target_directory and its subfolders for HTML files and generates a dynamic index.html
    with a modern, professional, and responsive app choosing screen.
    """
    
    app_files_with_paths = [] # List of (relative_path, subfolder_name)
    
    # Ensure target_directory exists and is accessible
    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' not found.")
        sys.exit(1)

    # Walk through the directory
    for root, dirs, files in os.walk(target_directory):
        # Calculate relative path from target_directory
        relative_root = os.path.relpath(root, target_directory)
        if relative_root == '.':
            subfolder_name = "" # Root directory
        else:
            subfolder_name = relative_root.replace('\\', '/') # Normalize path separators

        for filename in files:
            if filename.endswith(".html") and filename != "index.html":
                full_path = os.path.join(relative_root, filename)
                # Normalize path separators for href
                normalized_path = full_path.replace('\\', '/')
                app_files_with_paths.append((normalized_path, subfolder_name))

    app_files_with_paths.sort(key=lambda x: x[0].lower()) # Sort by path for consistent order

    app_cards_html = []
    for file_path, subfolder_name in app_files_with_paths:
        # Extract base filename for naming
        base_filename = os.path.basename(file_path)
        name_parts = []
        if subfolder_name:
            name_parts.append(subfolder_name.upper()) # Display subfolder name
        name_parts.append(base_filename.replace('.html', '').replace('-', ' ').upper())
        
        display_name = " / ".join(name_parts)
        
        # Determine icon based on name keywords (for flair)
        icon = '📄'
        if 'NBA' in display_name: icon = '🏀'
        elif 'NFL' in display_name: icon = '🏈'
        elif 'MLB' in display_name: icon = '⚾'
        elif 'WEATHER' in display_name or ('MAP' in display_name and 'WEATHER' in display_name): icon = '🌦️'
        elif 'GAME' in display_name or 'FLIP' in display_name or 'QWINGO' in display_name: icon = '🎲'
        elif 'LOGOMAP' in display_name: icon = '🗺️'
        elif 'PHOTO' in display_name: icon = '📸'
        elif 'PANEL' in display_name: icon = '🖥️'
        elif 'API' in display_name: icon = '🔌'
        elif 'AIRPORT' in display_name: icon = '✈️'
        elif 'RECEIPT' in display_name: icon = '🧾'
        elif 'SPORTS' in display_name: icon = '🏆'
        
        card_html = f"""
            <a href="{file_path}" class="glass-tile rounded-2xl p-6 flex flex-col items-center justify-center gap-4 text-center group h-40">
                <div class="text-4xl group-hover:scale-110 transition-transform duration-300 drop-shadow-2xl filter">{icon}</div>
                <div class="w-full">
                    <div class="text-xs font-black text-white tracking-wider truncate w-full group-hover:text-blue-400 transition-colors">{display_name}</div>
                </div>
            </a>
        """
        app_cards_html.append(card_html)

    full_html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local App Launcher</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ 
            font-family: 'Inter', sans-serif; 
            background-color: #020617; 
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.1) 0px, transparent 50%), 
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.1) 0px, transparent 50%);
            color: #f8fafc; 
            min-height: 100vh;
        }}
        
        .glass-tile {{
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .glass-tile:hover {{
            background: rgba(30, 41, 59, 0.7);
            border-color: rgba(56, 189, 248, 0.3);
            transform: translateY(-4px);
            box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
        }}
    </style>
</head>
<body class="p-6 md:p-12 flex flex-col gap-8">

    <!-- Header -->
    <header class="flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-slate-800 rounded-2xl flex items-center justify-center text-blue-400 font-black text-2xl shadow-xl border border-slate-700">
                🚀
            </div>
            <div>
                <h1 class="text-3xl font-black uppercase tracking-tighter text-white">App Launcher</h1>
                <p class="text-xs font-bold text-slate-500 uppercase tracking-widest">Dynamic Local Index</p>
            </div>
        </div>
        <div class="text-xs font-mono text-slate-500">{len(app_files_with_paths)} Apps Detected</div>
    </header>

    <!-- App Grid -->
    <main id="app-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        {"".join(app_cards_html)}
    </main>

</body>
</html>
    """

    output_path = os.path.join(target_directory, "index.html")
    with open(output_path, "w") as f:
        f.write(full_html_content)
    
    print(f"Generated index.html with {len(app_files_with_paths)} apps in {output_path}")

if __name__ == "__main__":
    # Ensure a directory is provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python generate_index.py <target_directory>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    generate_index_html(target_dir)
