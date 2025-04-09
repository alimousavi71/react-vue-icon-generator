import os
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext, messagebox
import json
from pathlib import Path
import re
from datetime import datetime

class SvgIconGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("SVG Icon Component Generator")
        self.root.geometry("900x750")
        
        # Configuration file path
        self.config_dir = os.path.join(os.path.expanduser("~"), ".svg_icon_generator")
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # Recent paths
        self.recent_source_paths = []
        self.recent_dest_paths = []
        
        # SVG files found in the source directory
        self.svg_files = []
        
        # Filtered SVG files list
        self.filtered_svg_files = []
        
        # Component prefix
        self.component_prefix = tk.StringVar(value="")
        
        # Component suffix
        self.component_suffix = tk.StringVar(value="Component")
        
        # Framework selection
        self.framework = tk.StringVar(value="Vue")
        
        # Search filter
        self.search_text = tk.StringVar(value="")
        
        # Load saved configuration
        self.load_config()
        
        # Source and destination folder paths
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        
        # Initialize UI
        self.setup_ui()
        
        # Bind path changes
        self.source_path.trace_add("write", self.on_source_path_change)
        self.source_combo.configure(textvariable=self.source_path)
        
        self.dest_path.trace_add("write", self.on_dest_path_change)
        self.dest_combo.configure(textvariable=self.dest_path)
        
        # Bind prefix/suffix changes to update component names in table
        self.component_prefix.trace_add("write", self.on_naming_change)
        self.component_suffix.trace_add("write", self.on_naming_change)
        
        # Update the combo boxes with recent paths
        self.update_recent_paths()
        
        # Update button text based on framework
        self.framework.trace_add("write", self.update_button_text)
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for folder selection
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=2)
        
        # Source folder selection
        source_frame = ttk.Frame(top_frame)
        source_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(source_frame, text="SVG Source:").pack(side=tk.LEFT, padx=2)
        
        # Source path dropdown
        self.source_combo = ttk.Combobox(source_frame, width=50)
        self.source_combo.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Browse source button
        source_btn = ttk.Button(source_frame, text="Browse", command=self.select_source_folder, width=8)
        source_btn.pack(side=tk.LEFT, padx=2)
        
        # Destination folder selection
        dest_frame = ttk.Frame(top_frame)
        dest_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(dest_frame, text="Output Dest:").pack(side=tk.LEFT, padx=2)
        
        # Destination path dropdown
        self.dest_combo = ttk.Combobox(dest_frame, width=50)
        self.dest_combo.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Browse destination button
        dest_btn = ttk.Button(dest_frame, text="Browse", command=self.select_dest_folder, width=8)
        dest_btn.pack(side=tk.LEFT, padx=2)
        
        # Component name settings
        name_frame = ttk.Frame(top_frame)
        name_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(name_frame, text="Component Prefix:").pack(side=tk.LEFT, padx=2)
        prefix_entry = ttk.Entry(name_frame, textvariable=self.component_prefix, width=10)
        prefix_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(name_frame, text="Component Suffix:").pack(side=tk.LEFT, padx=2)
        suffix_entry = ttk.Entry(name_frame, textvariable=self.component_suffix, width=15)
        suffix_entry.pack(side=tk.LEFT, padx=2)
        
        # Framework selection
        ttk.Label(name_frame, text="Framework:").pack(side=tk.LEFT, padx=2)
        framework_combo = ttk.Combobox(name_frame, textvariable=self.framework, width=10, state="readonly")
        framework_combo['values'] = ("Vue", "React")
        framework_combo.pack(side=tk.LEFT, padx=2)
        
        # File filter
        filter_frame = ttk.Frame(top_frame)
        filter_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=2)
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_text, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        self.search_text.trace_add("write", self.on_search_change)
        
        clear_btn = ttk.Button(filter_frame, text="Clear", command=self.clear_search, width=5)
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # Tab 1: Files list
        files_tab = ttk.Frame(notebook)
        notebook.add(files_tab, text="SVG Files")
        
        # Files tree view frame
        tree_frame = ttk.Frame(files_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Treeview for SVG files
        self.file_tree = ttk.Treeview(tree_frame, columns=("Path", "ComponentName"))
        self.file_tree.heading("#0", text="", anchor=tk.W)
        self.file_tree.heading("Path", text="SVG Path", anchor=tk.W)
        self.file_tree.heading("ComponentName", text="Component Name", anchor=tk.W)
        self.file_tree.column("#0", width=0, stretch=tk.NO)
        self.file_tree.column("Path", width=400, stretch=tk.YES)
        self.file_tree.column("ComponentName", width=300, stretch=tk.YES)
        
        # Scrollbars for treeview
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=vsb.set)
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.file_tree.xview)
        self.file_tree.configure(xscrollcommand=hsb.set)
        
        # Pack scrollbars and treeview
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.file_tree.bind("<<TreeviewSelect>>", self.on_file_selected)
        
        # Tab 2: Component Preview
        preview_tab = ttk.Frame(notebook)
        notebook.add(preview_tab, text="Component Preview")
        
        # Preview text area
        self.preview_area = scrolledtext.ScrolledText(preview_tab, wrap=tk.WORD)
        self.preview_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Tab 3: Log
        log_tab = ttk.Frame(notebook)
        notebook.add(log_tab, text="Log")
        
        # Log text area
        self.log_area = scrolledtext.ScrolledText(log_tab, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Generate button
        generate_frame = ttk.Frame(main_frame)
        generate_frame.pack(fill=tk.X, pady=5)
        
        self.generate_btn = ttk.Button(
            generate_frame, 
            text="Generate Vue Components", 
            command=self.generate_components,
            width=25
        )
        self.generate_btn.pack(side=tk.LEFT, padx=2)
        
        self.open_folder_btn = ttk.Button(
            generate_frame,
            text="Open Output Folder",
            command=self.open_output_folder,
            width=20
        )
        self.open_folder_btn.pack(side=tk.LEFT, padx=2)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=2)
        
    def update_button_text(self, *args):
        framework = self.framework.get()
        selection = self.file_tree.selection()
        
        if selection:
            self.generate_btn.config(text=f"Generate {framework} Components ({len(selection)} selected)")
        else:
            self.generate_btn.config(text=f"Generate {framework} Components")
        
    def load_config(self):
        try:
            # Create config directory if it doesn't exist
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir)
                
            # Load config if it exists
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.recent_source_paths = config.get('recent_source_paths', [])
                    self.recent_dest_paths = config.get('recent_dest_paths', [])
                    self.component_prefix.set(config.get('component_prefix', ''))
                    self.component_suffix.set(config.get('component_suffix', 'Component'))
                    self.framework.set(config.get('framework', 'Vue'))
        except Exception as e:
            self.log(f"Error loading config: {e}")
            self.recent_source_paths = []
            self.recent_dest_paths = []
            
    def save_config(self):
        try:
            config = {
                'recent_source_paths': self.recent_source_paths,
                'recent_dest_paths': self.recent_dest_paths,
                'component_prefix': self.component_prefix.get(),
                'component_suffix': self.component_suffix.get(),
                'framework': self.framework.get()
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            self.log(f"Error saving config: {e}")
            
    def update_recent_paths(self):
        self.source_combo['values'] = self.recent_source_paths
        self.dest_combo['values'] = self.recent_dest_paths
        
    def add_to_recent_source_paths(self, path):
        # Remove if already exists
        if path in self.recent_source_paths:
            self.recent_source_paths.remove(path)
            
        # Add to beginning of list
        self.recent_source_paths.insert(0, path)
        
        # Keep only the most recent 10 paths
        self.recent_source_paths = self.recent_source_paths[:10]
        
        # Update dropdown and save config
        self.update_recent_paths()
        self.save_config()
        
    def add_to_recent_dest_paths(self, path):
        # Remove if already exists
        if path in self.recent_dest_paths:
            self.recent_dest_paths.remove(path)
            
        # Add to beginning of list
        self.recent_dest_paths.insert(0, path)
        
        # Keep only the most recent 10 paths
        self.recent_dest_paths = self.recent_dest_paths[:10]
        
        # Update dropdown and save config
        self.update_recent_paths()
        self.save_config()
        
    def select_source_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.source_path.set(folder_selected)
            self.add_to_recent_source_paths(folder_selected)
            
    def select_dest_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.dest_path.set(folder_selected)
            self.add_to_recent_dest_paths(folder_selected)
            
    def on_source_path_change(self, *args):
        path = self.source_path.get()
        if path and os.path.isdir(path):
            self.scan_svg_files(path)
            
    def on_dest_path_change(self, *args):
        # Nothing to do here for now
        pass
    
    def on_search_change(self, *args):
        self.refresh_file_list()
        
    def on_naming_change(self, *args):
        # When prefix or suffix changes, update the component names in the table
        self.refresh_file_list()
        
    def clear_search(self):
        self.search_text.set("")
        
    def scan_svg_files(self, folder_path):
        # Clear previous file list
        self.file_tree.delete(*self.file_tree.get_children())
        self.svg_files.clear()
        self.filtered_svg_files.clear()
        
        # Log start of scanning
        self.log(f"Scanning for SVG files in: {folder_path} (including subfolders)")
        
        # Find all SVG files in the folder and all subfolders (with recursion)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Skip hidden files
                if file.startswith('.'):
                    continue
                    
                if file.lower().endswith('.svg'):
                    # Full path to the file
                    file_path = os.path.join(root, file)
                    
                    # Calculate relative path from the source folder
                    rel_path = os.path.relpath(file_path, folder_path)
                    
                    # Store file info
                    self.svg_files.append((file_path, rel_path))
        
        # Log number of files found
        self.log(f"Found {len(self.svg_files)} SVG files")
        
        # Display files in the treeview
        self.refresh_file_list()
        
        self.status_var.set(f"Found {len(self.svg_files)} SVG files in {folder_path} and subfolders")
        
    def get_component_name(self, rel_path):
        # Remove extension
        path_no_ext = os.path.splitext(rel_path)[0]
        
        # Replace path separators with nothing (to flatten the structure)
        path_parts = re.split(r'[/\\]', path_no_ext)
        
        # Process each part - split by any non-alphanumeric character and capitalize each word
        processed_parts = []
        for part in path_parts:
            # Split by spaces, underscores, hyphens, etc.
            words = re.split(r'[^a-zA-Z0-9]', part)
            for word in words:
                if word:  # Skip empty strings
                    # Capitalize the first letter of each word
                    processed_parts.append(word[0].upper() + word[1:] if len(word) > 1 else word.upper())
        
        # Join all parts with no spaces
        component_name = ''.join(processed_parts)
        
        # Add prefix and suffix
        prefix = self.component_prefix.get()
        suffix = self.component_suffix.get()
        
        return f"{prefix}{component_name}{suffix}"
        
    def refresh_file_list(self):
        # Clear the current view
        self.file_tree.delete(*self.file_tree.get_children())
        self.filtered_svg_files.clear()
        
        # Get search filter
        search = self.search_text.get().strip().lower()
        
        # Add files to the treeview based on filter
        for file_path, rel_path in self.svg_files:
            # Filter by search text
            if search and search not in rel_path.lower():
                continue
                
            # Get component name
            component_name = self.get_component_name(rel_path)
            
            # Add to treeview
            self.file_tree.insert(
                "", 
                "end", 
                values=(rel_path, component_name),
                tags=(file_path,)
            )
            
            # Add to filtered list
            self.filtered_svg_files.append((file_path, rel_path, component_name))
        
        # Update status
        if search:
            self.status_var.set(f"Displaying {len(self.filtered_svg_files)} of {len(self.svg_files)} SVG files (filter: '{search}')")
        else:
            self.status_var.set(f"Displaying all {len(self.svg_files)} SVG files")
    
    def on_file_selected(self, event):
        # Get selected items
        selection = self.file_tree.selection()
        if not selection:
            return
            
        # Update button text with selection count
        framework = self.framework.get()
        self.generate_btn.config(text=f"Generate {framework} Components ({len(selection)} selected)")
            
        # If only one item is selected, show its preview
        if len(selection) == 1:
            item = selection[0]
            file_path = self.file_tree.item(item, "tags")[0]
            rel_path = self.file_tree.item(item)['values'][0]
            component_name = self.file_tree.item(item)['values'][1]
            
            # Generate preview for this file
            self.generate_preview(file_path, rel_path, component_name)
        
    def generate_preview(self, file_path, rel_path, component_name):
        try:
            # Read SVG file
            with open(file_path, 'r', encoding='utf-8') as file:
                svg_content = file.read()
                
            # Generate component based on selected framework
            if self.framework.get() == "Vue":
                component_content = self.create_vue_component(svg_content, rel_path, component_name)
            else:
                component_content = self.create_react_component(svg_content, rel_path, component_name)
            
            # Update preview
            self.preview_area.delete(1.0, tk.END)
            self.preview_area.insert(tk.END, component_content)
            
            self.log(f"Generated {self.framework.get()} preview for {rel_path}")
        except Exception as e:
            self.log(f"Error generating preview for {rel_path}: {str(e)}")
            self.preview_area.delete(1.0, tk.END)
            self.preview_area.insert(tk.END, f"Error generating preview: {str(e)}")
    
    def extract_svg_details(self, svg_content):
        # Use regex to extract viewBox attribute and clean SVG
        viewbox_match = re.search(r'viewBox=["\'](.*?)["\']', svg_content)
        viewbox = viewbox_match.group(1) if viewbox_match else "0 0 24 24"
        
        # Remove <?xml ... ?> declarations if present
        svg_content = re.sub(r'<\?xml.*?\?>', '', svg_content)
        
        # Extract the actual SVG content (everything between <svg> and </svg>)
        svg_inner_match = re.search(r'<svg[^>]*>(.*?)</svg>', svg_content, re.DOTALL)
        svg_inner_content = svg_inner_match.group(1).strip() if svg_inner_match else svg_content
        
        # Clean up unnecessary attributes
        svg_inner_content = re.sub(r'xmlns(:xlink)?=".*?"', '', svg_inner_content)
        svg_inner_content = re.sub(r'xml:space=".*?"', '', svg_inner_content)
        
        return viewbox, svg_inner_content
    
    def create_vue_component(self, svg_content, rel_path, component_name):
        try:
            # Extract SVG details
            viewbox, svg_inner_content = self.extract_svg_details(svg_content)
            
            # Create Vue component
            timestamp = datetime.now().strftime("%Y-%m-%d")
            component_template = f"""<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    :width="size"
    :height="size"
    :stroke-width="strokeWidth"
    :fill="filled ? 'currentColor' : 'none'"
    stroke="currentColor"
    viewBox="{viewbox}"
    :class="customClass"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    {svg_inner_content}
  </svg>
</template>

<script>
/**
 * {component_name}
 * Generated from: {rel_path}
 * Date: {timestamp}
 */
export default {{
  name: '{component_name}',
  props: {{
    size: {{
      type: [Number, String],
      default: 24
    }},
    strokeWidth: {{
      type: [Number, String],
      default: 1.5
    }},
    filled: {{
      type: Boolean,
      default: false
    }},
    customClass: {{
      type: String,
      default: ''
    }}
  }}
}}
</script>
"""
            return component_template
            
        except Exception as e:
            raise Exception(f"Error processing SVG: {str(e)}")
    
    def create_react_component(self, svg_content, rel_path, component_name):
        try:
            # Extract SVG details
            viewbox, svg_inner_content = self.extract_svg_details(svg_content)
            
            # Create React component
            timestamp = datetime.now().strftime("%Y-%m-%d")
            component_template = f"""import React from 'react';

/**
 * {component_name}
 * Generated from: {rel_path}
 * Date: {timestamp}
 */
const {component_name} = ({{ 
  size = 24, 
  strokeWidth = 1.5, 
  filled = false, 
  className = '', 
  ...props 
}}) => {{
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={{size}}
      height={{size}}
      strokeWidth={{strokeWidth}}
      fill={{filled ? 'currentColor' : 'none'}}
      stroke="currentColor"
      viewBox="{viewbox}"
      className={{className}}
      strokeLinecap="round"
      strokeLinejoin="round"
      {{...props}}
    >
      {svg_inner_content}
    </svg>
  );
}};

export default {component_name};
"""
            return component_template
            
        except Exception as e:
            raise Exception(f"Error processing SVG: {str(e)}")
    
    def log(self, message):
        # Add timestamp to message
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Update log text area
        self.log_area.insert(tk.END, log_entry + "\n")
        self.log_area.see(tk.END)  # Scroll to the end
        
    def generate_components(self):
        # Validate paths
        source_path = self.source_path.get()
        dest_path = self.dest_path.get()
        framework = self.framework.get()
        
        if not source_path or not os.path.isdir(source_path):
            self.status_var.set("Please select a valid source folder")
            return
            
        if not dest_path or not os.path.isdir(dest_path):
            self.status_var.set("Please select a valid destination folder")
            return
            
        # Get selected items from the treeview
        selected_items = self.file_tree.selection()
        if not selected_items:
            self.status_var.set("Please select SVG files to generate components for")
            return
        
        # Get the selected files information
        selected_files = []
        for item in selected_items:
            file_path = self.file_tree.item(item, "tags")[0]
            rel_path = self.file_tree.item(item)['values'][0]
            component_name = self.file_tree.item(item)['values'][1]
            selected_files.append((file_path, rel_path, component_name))
            
        # Log start of generation
        self.log(f"Starting {framework} component generation for {len(selected_files)} selected SVG files")
        self.log(f"Output folder: {dest_path}")
        
        # Ask if user wants to preserve directory structure
        preserve_structure = messagebox.askyesno(
            "Preserve Directory Structure",
            "Do you want to preserve the directory structure in the output folder?"
        )
        
        # Create index file for exporting all components
        file_extension = "js" if framework == "React" else "js"
        index_content = [
            "/**",
            f" * Auto-generated index file for SVG icon components",
            f" * Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            " */", 
            ""
        ]
        
        # Track success and failures
        success_count = 0
        failure_count = 0
        
        # Process each selected SVG file
        for file_path, rel_path, component_name in selected_files:
            try:
                # Read SVG file
                with open(file_path, 'r', encoding='utf-8') as file:
                    svg_content = file.read()
                
                # Determine output path based on whether to preserve directory structure
                if preserve_structure and os.path.dirname(rel_path):
                    # Create subdirectories to match source structure
                    sub_dir = os.path.dirname(rel_path)
                    output_dir = os.path.join(dest_path, sub_dir)
                    os.makedirs(output_dir, exist_ok=True)
                    self.log(f"Created subdirectory: {sub_dir}")
                else:
                    output_dir = dest_path
                
                # Generate component based on selected framework
                if framework == "Vue":
                    component_content = self.create_vue_component(svg_content, rel_path, component_name)
                    output_path = os.path.join(output_dir, f"{component_name}.vue")
                    path_for_import = os.path.join(os.path.dirname(rel_path), component_name).replace("\\", "/") if preserve_structure else component_name
                    index_content.append(f"export {{ default as {component_name} }} from './{path_for_import}.vue';")
                else:
                    component_content = self.create_react_component(svg_content, rel_path, component_name)
                    output_path = os.path.join(output_dir, f"{component_name}.jsx")
                    path_for_import = os.path.join(os.path.dirname(rel_path), component_name).replace("\\", "/") if preserve_structure else component_name
                    index_content.append(f"export {{ default as {component_name} }} from './{path_for_import}';")
                
                # Create the output file
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(component_content)
                
                # Log success
                self.log(f"Generated: {os.path.basename(output_path)}")
                success_count += 1
                
            except Exception as e:
                self.log(f"Error processing {rel_path}: {str(e)}")
                failure_count += 1
                
            # Update status after each file
            self.status_var.set(f"Processed {success_count + failure_count} of {len(selected_files)} files...")
            self.root.update()  # Force UI update
        
        # Write index file
        try:
            index_path = os.path.join(dest_path, f"index.{file_extension}")
            with open(index_path, 'w', encoding='utf-8') as index_file:
                index_file.write("\n".join(index_content))
            self.log(f"Generated index.{file_extension} with {success_count} component exports")
        except Exception as e:
            self.log(f"Error generating index.{file_extension}: {str(e)}")
        
        # Final status update
        self.status_var.set(f"Completed: {success_count} {framework} components generated, {failure_count} failures")
        self.log(f"{framework} component generation completed")
        
    def open_output_folder(self):
        dest_path = self.dest_path.get()
        if not dest_path or not os.path.isdir(dest_path):
            self.status_var.set("No valid destination folder selected")
            return
            
        # Open the folder in file explorer
        try:
            if os.name == 'nt':  # Windows
                os.startfile(dest_path)
            elif os.name == 'posix':  # macOS and Linux
                import subprocess
                if os.path.exists('/usr/bin/open'):  # macOS
                    subprocess.Popen(['open', dest_path])
                else:  # Linux
                    subprocess.Popen(['xdg-open', dest_path])
            
            self.log(f"Opened output folder: {dest_path}")
        except Exception as e:
            self.log(f"Error opening folder: {str(e)}")
        
def main():
    root = tk.Tk()
    app = SvgIconGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()