## 🛠️ Troubleshooting

### 🧩 iframe overflow

If the embedded iframe is too large and causes scroll bars to appear, this can be adjusted from the **display size settings** in **Tableau** or **Power BI**.

- In **Tableau**, go to `Dashboard > Size` and select **Automatic** or set a custom size that fits the embed container.
- In **Power BI**, go to the **Page Size** section in the Format panel and choose a layout like **16:9** or set a **Custom** width/height to better fit the iframe.

Adjusting these settings helps the report/dashboard fit properly without showing unwanted scroll bars in the iframe.


## 📊 Report Size in **Power BI**

In Power BI, the report size affects how it appears on the **user's screen**, in **Power BI Service**, or when it is **embedded on a website**.

---

### 📏 Available Size Options:

#### 🔹 Page Size

Power BI allows you to set the **page size** from the canvas formatting section:

- **16:9 (Widescreen)** *(default)*  
- **4:3 (Standard screen)**  
- **Cortado (Cropped view for mobile or specific visuals)**  
- **Custom**: You can set the **width and height in pixels**, such as `1200 x 900 px`.

#### 🔹 Responsive View
- When embedded on the web or viewed in Power BI Service, the report can **automatically adjust** to the size of the container (responsive).
- In **Power BI Embedded**, you can control the size using CSS and HTML containers.

---

### 🛠️ Where to configure it?

In **Power BI Desktop**:  
Visualizations > Click outside the canvas > Format panel (paintbrush icon) > Page Size

1. Choose a type (16:9, 4:3, Cortado, Custom)  
2. If custom, set width and height in pixels

---

### 💡 Helpful Tip:

- For **mobile devices**, you can create a **specific mobile layout** from the menu:
- View > View as > Mobile layout

---

## 🖼️ Dashboard Size in Tableau

In Tableau, each dashboard has a size setting that affects how it appears on different screens. This is especially important if you're going to **publish it on Tableau Server or Tableau Public**, or **embed it on a website**.

---

### 📏 Types of Dashboard Size:

#### 🔹 Fixed Size
- You choose a specific **width and height**, for example: `1200 x 800 px`.
- Ideal if you know exactly which device or screen it will be viewed on.

#### 🔹 Automatic
- Tableau **automatically adjusts the dashboard size** to fit the container where it's displayed.
- It may **distort** if the layout wasn't designed flexibly.

#### 🔹 Range
- You can define a **minimum and maximum** width/height, and Tableau adjusts the dashboard within that range.
- Useful for dashboards **embedded on websites** or when screen sizes may vary.

---

### 🛠️ Where to configure it?

In **Tableau Desktop**: Right-hand menu > Dashboard > Size  
1. Select: **Fixed**, **Automatic**, or **Range**  (Choose *Automatic* to make it adjust on its own)  
2. Then, define the **height/width values** if applicable

![image](https://github.com/user-attachments/assets/7d1d0003-4897-419b-981a-2ae8855fe96b)
