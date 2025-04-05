# 🎨 SVG Icon Component Generator

<img width="900" alt="image" src="https://github.com/user-attachments/assets/b0ae6661-646d-4c75-92ed-425d6a9215b7" />

> Convert your SVG icons into Vue or React components with just a few clicks!

## ✨ Features

- 🔄 **Framework Support**: Generate components for both Vue and React
- 🔍 **Preview Components**: See how your component will look before generating
- 📦 **Batch Processing**: Select multiple SVG files to process at once
- 🏷️ **Custom Naming**: Add prefixes and suffixes to component names
- 🔎 **File Filtering**: Easily find specific icons with the search feature
- 📝 **Auto-Generated Index**: Creates an index file for easy importing
- 💾 **Configuration Saving**: Remembers your paths and settings between sessions

## 📸 Screenshot

![Application Screenshot](https://via.placeholder.com/800x600?text=SVG+Icon+Component+Generator)

## 🚀 Getting Started

### Prerequisites

- 🐍 Python 3.6 or higher
- Tkinter (usually included with Python)

### Installation

1. Clone this repository or download the script:

```bash
git clone https://github.com/yourusername/svg-icon-generator.git
```

2. Navigate to the directory:

```bash
cd svg-icon-generator
```

3. Run the script:

```bash
python svg_icon_generator.py
```

## 🔧 How to Use

1. **Select Source Folder** 📂

   - Click "Browse" next to "SVG Source" to select the folder containing your SVG files

2. **Select Output Destination** 📝

   - Click "Browse" next to "Output Dest" to choose where to save the generated components

3. **Choose Framework** ⚛️

   - Select either "Vue" or "React" from the dropdown menu

4. **Customize Component Names** (Optional) 🏷️

   - Add a prefix and/or suffix to your component names

5. **Select SVG Files** 🖱️

   - Click on the SVG files you want to convert in the list
   - Use Ctrl+click or Shift+click to select multiple files

6. **Preview Component** 👁️

   - When a single file is selected, you can see a preview of the generated component

7. **Generate Components** ⚙️

   - Click the "Generate Components" button to create your selected components

8. **Check Output** ✅
   - Click "Open Output Folder" to view your newly created components

## 📋 Component Output Format

### Vue Components (.vue)

```vue
<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    :width="size"
    :height="size"
    :stroke-width="strokeWidth"
    :fill="filled ? 'currentColor' : 'none'"
    stroke="currentColor"
    viewBox="0 0 24 24"
    :class="customClass"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <!-- SVG content here -->
  </svg>
</template>

<script>
export default {
  name: "IconComponent",
  props: {
    size: {
      type: [Number, String],
      default: 24,
    },
    strokeWidth: {
      type: [Number, String],
      default: 1.5,
    },
    filled: {
      type: Boolean,
      default: false,
    },
    customClass: {
      type: String,
      default: "",
    },
  },
};
</script>
```

### React Components (.jsx)

```jsx
import React from "react";

const IconComponent = ({
  size = 24,
  strokeWidth = 1.5,
  filled = false,
  className = "",
  ...props
}) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      strokeWidth={strokeWidth}
      fill={filled ? "currentColor" : "none"}
      stroke="currentColor"
      viewBox="0 0 24 24"
      className={className}
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      {/* SVG content here */}
    </svg>
  );
};

export default IconComponent;
```

## 📦 Generated Index File

The tool automatically generates an index file to easily import all components:

```javascript
// index.js
export { default as Icon1Component } from "./Icon1Component.vue";
export { default as Icon2Component } from "./Icon2Component.vue";
// And so on...
```

## 🛠️ Advanced Usage

### Filtering SVG Files

- Use the filter field to search for specific SVG files by name
- Clear the filter by clicking the "Clear" button

### Recent Paths

- The application saves your recent source and destination paths
- Access them through the dropdown menus for quick selection

## 🔍 Troubleshooting

### No SVG Files Found

- Ensure your source folder contains `.svg` files
- Check that the files have the `.svg` extension (case sensitive)

### Error Processing SVG

- Verify that your SVG files are properly formatted
- Try opening and resaving the SVG in a vector editor like Inkscape or Adobe Illustrator

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 💖 Acknowledgements

- Thanks to all the open-source projects that made this tool possible
- Icons used in the example are from [Various Icon Libraries]

---

Made with ❤️ by [Your Name]
