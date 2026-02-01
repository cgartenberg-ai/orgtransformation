import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Botanical palette
        forest: {
          DEFAULT: "#1B4332",
          50: "#E8F0EC",
          100: "#C5D9CE",
          200: "#9FBFAD",
          300: "#79A68C",
          400: "#5C9173",
          500: "#3F7D5A",
          600: "#336A4C",
          700: "#27573E",
          800: "#1B4332",
          900: "#0D2119",
        },
        cream: {
          DEFAULT: "#FAF3E0",
          50: "#FFFDF7",
          100: "#FDF8ED",
          200: "#FAF3E0",
          300: "#F2E4C3",
          400: "#E9D5A6",
          500: "#E0C689",
        },
        amber: {
          DEFAULT: "#D4A373",
          50: "#FBF3EB",
          100: "#F5E1CE",
          200: "#ECCFB0",
          300: "#E2BD93",
          400: "#D4A373",
          500: "#C48B55",
          600: "#A87241",
          700: "#835933",
          800: "#5E4025",
          900: "#392717",
        },
        sage: {
          DEFAULT: "#84A98C",
          50: "#EFF4F0",
          100: "#D8E5DB",
          200: "#BFD4C4",
          300: "#A5C3AD",
          400: "#84A98C",
          500: "#6B9474",
          600: "#577A5F",
          700: "#43604A",
          800: "#2F4635",
          900: "#1B2C20",
        },
        charcoal: {
          DEFAULT: "#2D3436",
          50: "#EAEAEB",
          100: "#CBCCCD",
          200: "#A9ABAC",
          300: "#878A8C",
          400: "#6D7071",
          500: "#535657",
          600: "#434546",
          700: "#383A3B",
          800: "#2D3436",
          900: "#1A1D1E",
        },
        // shadcn/ui semantic colors mapped to botanical palette
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      fontFamily: {
        serif: ["var(--font-fraunces)", "Georgia", "serif"],
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
