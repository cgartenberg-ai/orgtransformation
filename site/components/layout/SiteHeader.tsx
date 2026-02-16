import Link from "next/link";

const navItems = [
  { href: "/specimens", label: "Specimens" },
  { href: "/taxonomy", label: "Taxonomy" },
  { href: "/framework", label: "Framework" },
  { href: "/findings", label: "Findings" },
  { href: "/mechanisms", label: "Principles" },
  { href: "/tensions", label: "Tensions" },
  { href: "/purpose-claims", label: "Purpose Claims" },
  { href: "/compare", label: "Compare" },
  { href: "/about", label: "About" },
];

export function SiteHeader() {
  return (
    <header className="border-b border-sage-200 bg-cream-50">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2">
          <span className="font-serif text-xl font-semibold text-forest">
            Field Guide to AI Organizations
          </span>
        </Link>
        <nav className="hidden items-center gap-6 md:flex">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-sm font-medium text-charcoal-600 transition-colors hover:text-forest"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
