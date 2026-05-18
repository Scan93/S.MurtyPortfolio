const SKILLS_DATA = [
  {
    name: "SQL / SSMS",
    category: "Analytics & Tools",
    description: "I use SQL as my primary tool for pulling, joining, and transforming data. Most of my experience is with SQL Server Management Studio — writing complex multi-table queries, CTEs, and aggregations to answer real operational questions, not just toy examples.",
    usedIn: [
      "CIS215 coursework — multi-table joins, subqueries, stored procedures",
      "Aerospace inventory work — ad hoc queries against MES and ERP data",
      "Sales Performance Analysis project — data extraction and transformation"
    ]
  },
  {
    name: "Python",
    aliases: ["python (pandas)", "pandas", "python/pandas"],
    category: "Analytics & Tools",
    description: "Python is my go-to for data pipelines and analysis. I'm most comfortable with pandas for data wrangling, matplotlib and seaborn for visualization, and building scripts that automate repetitive reporting tasks.",
    usedIn: [
      "Sales Performance Analysis — 545K row dataset, full ETL pipeline in pandas",
      "Finance Project — automated PDF report generator with personal account data",
      "SIGNAL market research agent — Anthropic API integration, report generation",
      "Job finder automation — Playwright-based LinkedIn Easy Apply bot"
    ]
  },
  {
    name: "Power BI",
    category: "Analytics & Tools",
    description: "I've worked with Power BI for building interactive dashboards and connecting to live data sources. I understand DAX basics and how to structure data models for reporting.",
    usedIn: [
      "CIS215 Business Intelligence coursework — dashboard design and DAX formulas",
      "Retail operations context — familiar with KPI reporting structures"
    ]
  },
  {
    name: "Excel / VBA",
    aliases: ["excel", "vba", "microsoft excel"],
    category: "Analytics & Tools",
    description: "Deep Excel experience from years of operational work — pivot tables, VLOOKUP/XLOOKUP, conditional formatting, and VBA macros for automating repetitive tasks. Excel is still the fastest tool for quick one-off analysis.",
    usedIn: [
      "Aerospace manufacturing — daily production tracking and reporting",
      "Retail operations — inventory count reconciliation and scheduling",
      "CIS215 coursework — advanced formulas and VBA automation"
    ]
  },
  {
    name: "Inventory Systems",
    category: "Inventory & Supply Chain",
    description: "I've worked directly inside inventory systems from both the operational and analytical side — receiving, cycle counts, discrepancy resolution, and the data layer underneath it all. I understand how inventory data gets dirty and how to clean it.",
    usedIn: [
      "Spirit AeroSystems — production inventory in aerospace manufacturing environment",
      "Target — retail inventory management, replenishment, and backroom operations",
      "StockBin (personal project) — built a material inventory web app from scratch"
    ]
  },
  {
    name: "Procurement",
    category: "Inventory & Supply Chain",
    description: "Hands-on procurement experience from the manufacturing floor — purchase orders, vendor coordination, shortage escalation, and understanding lead time impacts on production schedules.",
    usedIn: [
      "Spirit AeroSystems — coordinated procurement for aerospace components",
      "Materials tracking and shortage resolution in production environment"
    ]
  },
  {
    name: "Materials Tracking",
    category: "Inventory & Supply Chain",
    description: "Tracking materials through a production lifecycle — from receipt to point-of-use — with full accountability for serialized and lot-controlled parts. I've worked with both paper-based and system-driven tracking.",
    usedIn: [
      "Spirit AeroSystems — serialized and lot-controlled aerospace components",
      "StockBin — designed the usage log and reorder workflow for the app"
    ]
  },
  {
    name: "Retail Operations",
    category: "Inventory & Supply Chain",
    description: "Multi-year experience running retail operations — stocking, replenishment, team coordination, shrink control, and the constant data work of reconciling what the system says versus what's actually on the shelf.",
    usedIn: [
      "Target — retail operations, team leadership, inventory reconciliation",
      "Informed data analysis perspective on retail datasets (Sales Performance project)"
    ]
  },
  {
    name: "Solumina MES",
    category: "Inventory & Supply Chain",
    description: "Solumina is a Manufacturing Execution System used in aerospace. I used it daily to manage work orders, track part status, and ensure production documentation compliance — a highly regulated environment where data accuracy is non-negotiable.",
    usedIn: [
      "Spirit AeroSystems — daily use for production work order management and part tracking"
    ]
  },
  {
    name: "Aerospace Manufacturing",
    category: "Domain Expertise",
    description: "I spent years working inside a Tier 1 aerospace supplier environment. I understand production workflows, quality requirements, AS9100 compliance culture, and what it actually costs when a part is missing or misidentified.",
    usedIn: [
      "Spirit AeroSystems — inventory, materials, and production support roles",
      "Provided real-world context for process optimization and data accuracy work"
    ]
  },
  {
    name: "Process Optimization",
    category: "Domain Expertise",
    description: "Finding inefficiencies and eliminating them — whether that's a manual reporting step that can be scripted, a counting process that introduces errors, or a workflow that hasn't been questioned in years. I do this with data, not just intuition.",
    usedIn: [
      "Aerospace manufacturing — identified and reduced recurring inventory discrepancies",
      "Finance Project — automated monthly reporting that was previously manual",
      "StockBin — designed the add-item flow around a 15-second usability target"
    ]
  },
  {
    name: "Quality Compliance",
    category: "Domain Expertise",
    description: "Working in aerospace means quality isn't optional. I'm familiar with documentation requirements, traceability standards, and the discipline of doing things right the first time because rework is expensive and safety is real.",
    usedIn: [
      "Spirit AeroSystems — part traceability, documentation, and compliance workflows"
    ]
  },
  {
    name: "Team Leadership",
    category: "Domain Expertise",
    description: "I've led small teams in high-pace operational environments — coordinating priorities, training new team members, and maintaining output quality under pressure. Leadership in those contexts is practical and direct.",
    usedIn: [
      "Target — led team operations across multiple departments",
      "Spirit AeroSystems — coordinated across production and materials teams"
    ]
  },
  {
    name: "Mechanical Sympathy",
    category: "Domain Expertise",
    description: "A concept from motorsport: understanding how a machine actually works makes you better at operating or analyzing it. My engineering background and hands-on work with physical systems gives me a hardware-grounded perspective that most pure data analysts don't have.",
    usedIn: [
      "Mechanical engineering studies — physical systems, tolerances, manufacturing processes",
      "3D printing and fabrication — personal projects requiring precision and iteration",
      "Pool chemistry calculator app — applied domain knowledge to real-world tooling"
    ]
  },
  {
    name: "JavaScript",
    aliases: ["js", "vanilla js", "vanilla javascript"],
    category: "Web Development",
    description: "I use vanilla JavaScript to build interactive web apps without frameworks. I'm comfortable with DOM manipulation, event handling, localStorage, fetch, and structuring logic for real usability.",
    usedIn: [
      "StockBin — complete app logic: CRUD, photo compression, usage tracking, export/import",
      "Portfolio website — interactive features, animations, cursor effects",
      "Analytics Hub — visitor counter, retro clock, overlay interactions"
    ]
  },
  {
    name: "HTML / CSS",
    aliases: ["html", "css", "html/css"],
    category: "Web Development",
    description: "Solid fundamentals in semantic HTML and CSS layout — flexbox, grid, responsive design, CSS variables, and animations. I design for mobile-first and care about polish.",
    usedIn: [
      "StockBin — full UI design from scratch, dark theme, mobile-first",
      "Portfolio website (sdmurty.com) — all pages designed and built by hand",
      "Sales Performance Analysis report page"
    ]
  },
  {
    name: "SwiftUI",
    category: "Mobile Development",
    description: "I've built functional iOS apps using SwiftUI — declarative layout, state management, and integrating device capabilities like the camera. Still growing in this area but I've shipped working apps.",
    usedIn: [
      "PoolCalc — K2005C chemical dosage calculator with barcode scanner, 11 sanitizer variants",
      "BarcodeVault — standalone barcode scanner app with camera layer fix",
      "MyFirstApp — learning sandbox, 4-tab shell"
    ]
  },
  {
    name: "Git / GitHub",
    aliases: ["git", "github", "version control"],
    category: "Web Development",
    description: "I use Git for version control on all my projects and GitHub for hosting, Pages deployment, and public portfolio work.",
    usedIn: [
      "StockBin — public repo, GitHub Pages deployment",
      "Portfolio website — GitHub Pages at sdmurty.com",
      "All personal projects tracked in Git"
    ]
  },
  {
    name: "Claude API / Anthropic SDK",
    aliases: ["anthropic", "claude api", "llm", "ai api"],
    category: "AI & Automation",
    description: "I've integrated the Claude API to build agentic tools — passing structured prompts, handling responses, and building useful output pipelines. Not just calling an API but thinking about what makes a good prompt and a useful result.",
    usedIn: [
      "SIGNAL — market research agent that generates full reports via Claude API",
      "Finance Project — considered for narrative generation in PDF reports"
    ]
  },
  {
    name: "Node.js",
    aliases: ["node", "nodejs"],
    category: "AI & Automation",
    description: "I use Node.js for scripting and backend tooling — running local agents, managing environment variables, and building terminal-based automation tools.",
    usedIn: [
      "SIGNAL market research agent — full Node.js CLI script"
    ]
  },
  {
    name: "Matplotlib / Seaborn",
    aliases: ["matplotlib", "seaborn", "data visualization", "data viz"],
    category: "Analytics & Tools",
    description: "Python visualization libraries I use to turn analysis into something readable. I focus on clarity over decoration — the chart should answer the question, not impress with complexity.",
    usedIn: [
      "Sales Performance Analysis — revenue trends, product breakdowns, customer segments"
    ]
  }
];
