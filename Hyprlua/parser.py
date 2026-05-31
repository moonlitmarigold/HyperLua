#!/usr/bin/env python3
"""
Simple parser for Hyprland config directory.
Counts and categorizes different types of configuration directives.
"""

import json
from pathlib import Path


def main(config_dir:Path):
    """Main entry point."""
    
    print("\n" + "="*70)
    print("HYPRLAND CONFIG PARSE RESULTS")
    print("="*70 + "\n")
    
    excluded_files = []
    totals = {
        'binds': 0,
        'windowrules': 0,
        'layerrules': 0,
        'workspaces': 0,
        'sources': 0,
        'options': 0
    }
    
    file_results = []
    
    for config_file in sorted(config_dir.glob('**/*.conf')):
        file_name = config_file.name
        
        # Exclude backup/old files
        if file_name.endswith('.old') or file_name.endswith('.copy') or file_name.endswith('~'):
            excluded_files.append(str(config_file.relative_to('/home/alex/.config/hypr')))
            continue
        
        # Read file
        content = config_file.read_text()
        lines = content.split('\n')
        
        file_results.append({
            'file': str(config_file.relative_to('/home/alex/.config/hypr')),
            'total_lines': len(lines)
        })
        
        # Count different directive types
        binds_count = 0
        wraps_count = 0  # windowrules
        lays_count = 0   # layerrules
        wss_count = 0    # workspace
        srcs_count = 0   # source =
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                continue
            
            # Count binds
            if stripped.startswith(('bind', 'bindi', 'bindm', 'bindd', 'bindel', 'bindl')):
                binds_count += 1
                totals['binds'] += 1
            
            # Count windowrules
            elif stripped.startswith('windowrule') or stripped.startswith('windowrulev2'):
                wraps_count += 1
                totals['windowrules'] += 1
            
            # Count layerrules
            elif stripped.startswith('layerrule'):
                lays_count += 1
                totals['layerrules'] += 1
            
            # Count workspace rules
            elif stripped.startswith('workspace ') and '{' in stripped:
                wss_count += 1
                totals['workspaces'] += 1
            
            # Count source links
            elif stripped.startswith('source ='):
                srcs_count += 1
                totals['sources'] += 1
        
        # Count options (key: value pairs)
        options_count = 0
        for line in lines:
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                continue
            
            # Skip if already counted as bind/rule/etc
            if stripped.startswith(('bind', 'windowrule', 'layerrule', 'workspace', 'source')):
                continue
            
            # Count key: value pairs
            if ':' in stripped and '=' not in stripped or 'exec ' in stripped:
                options_count += 1
                totals['options'] += 1
        
        file_results[-1]['binds'] = binds_count
        file_results[-1]['windowrules'] = wraps_count
        file_results[-1]['layerrules'] = lays_count
        file_results[-1]['workspaces'] = wss_count
        file_results[-1]['sources'] = srcs_count
        file_results[-1]['options'] = options_count
    
    print(f"Files parsed: {len(file_results)}")
    print(f"Excluded files: {len(excluded_files)}")
    if excluded_files:
        print(f"  {', '.join(excluded_files)}")
    
    print(f"\n{'='*70}")
    print("SUMMARY BY DIRECTIVE TYPE")
    print(f"{'='*70}")
    print(f"\nBinds: {totals['binds']}")
    print(f"Window rules: {totals['windowrules']}")
    print(f"Layer rules: {totals['layerrules']}")
    print(f"Workspace rules: {totals['workspaces']}")
    print(f"Source links: {totals['sources']}")
    print(f"Configuration options: {totals['options']}")
    
    print(f"\n{'='*70}")
    print("FILE-BY-FILE BREAKDOWN")
    print(f"{'='*70}")
    
    for result in file_results:
        file_lines = result['file']
        f_binds = result['binds']
        f_wr = result['windowrules']
        f_lay = result['layerrules']
        f_ws = result['workspaces']
        f_src = result['sources']
        f_opt = result['options']
        
        print(f"\n{file_lines}:")
        print(f"  Lines: {result['total_lines']}")
        print(f"  Binds: {f_binds}")
        print(f"  Window rules: {f_wr}")
        print(f"  Layer rules: {f_lay}")
        print(f"  Workspace rules: {f_ws}")
        print(f"  Source links: {f_src}")
        print(f"  Options: {f_opt}")
    
    print(f"\n{'='*70}")
    print("COMPLETE DATA (JSON)")
    print(f"{'='*70}")
    
    # Prepare JSON output
    json_data = {
        'total_files': len(file_results),
        'excluded_files': excluded_files,
        'totals': totals,
        'files': []
    }
    
    for r in file_results:
        json_data['files'].append({
            'file': r['file'],
            'lines': r['total_lines'],
            'binds': r['binds'],
            'windowrules': r['windowrules'],
            'layerrules': r['layerrules'],
            'workspaces': r['workspaces'],
            'sources': r['sources'],
            'options': r['options']
        })
    
    print(json.dumps(json_data, indent=2))
    
    print("\n" + "="*70)
    print("PARSING COMPLETE")
    print("="*70 + "\n")


