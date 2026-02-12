---
name: ultimate-frontend-design
description: Master comprehensive frontend design and development covering visual design foundations, design systems, responsive layouts, component architecture, interaction patterns, and mobile development. Use when building any frontend interface, web application, or cross-platform mobile app that requires professional-grade design and implementation.
---

# Ultimate Frontend Design

A comprehensive, production-grade design system and development framework covering all aspects of modern frontend engineering - from visual foundations to mobile deployment.

## Quick Start Overview

### When to Use This Skill

| Task Domain | Keywords | Use Cases |
|-------------|-------------|------------|
| **Visual Design** | typography, color, spacing, iconography, branding | Establishing design tokens, style guides, visual hierarchy |
| **Design Systems** | tokens, theming, components, scalability | Building component libraries, multi-brand systems |
| **Responsive Design** | mobile-first, breakpoints, container queries | Adaptive interfaces, fluid layouts, cross-device |
| **Component Design** | React, Vue, Svelte, composition patterns | Reusable components, design systems |
| **Interaction Design** | animations, transitions, microinteractions | User feedback, delightful experiences |
| **Mobile** | iOS, Android, React Native, navigation | Cross-platform apps, native patterns |

### Core Pillars

```
Visual Foundation → Design System → Component Architecture → Responsive + Interactive → Cross-Platform
       ↓                   ↓                    ↓                        ↓                    ↓
   Typography          Tokens              Composition             Container Queries       Platform Patterns
   Color Theory        Theming              Compound                Fluid Layouts           iOS (SwiftUI)
   Spacing Systems     Semantic Tokens      Slots/Props              Breakpoints            Android (Material)
   Iconography         Multi-brand           Render Props             Viewport Units          React Native
```

### Domain Coverage

| Domain | Key Topics | Output |
|---------|-------------|---------|
| [Visual Design](#visual-design-foundations) | Typography, color, spacing, iconography | Design tokens, style guides, visual systems |
| [Design Systems](#design-systems) | Tokens, theming, architecture, pipelines | Scalable design systems, brand consistency |
| [Responsive Design](#responsive-design) | Container queries, fluid layouts, breakpoints | Adaptive interfaces, mobile-first layouts |
| [Component Design](#component-design) | Patterns, composition, styling, APIs | Reusable component libraries |
| [Interaction Design](#interaction-design) | Motion, feedback, timing, accessibility | Delightful user experiences |
| [Mobile Development](#mobile-development) | iOS, Android, React Native, navigation | Cross-platform mobile applications |

---

## Table of Contents

1. [Visual Design Foundations](#visual-design-foundations)
2. [Design Systems](#design-systems)
3. [Responsive Design](#responsive-design)
4. [Component Design](#component-design)
5. [Interaction Design](#interaction-design)
6. [Mobile Development](#mobile-development)
7. [Implementation Checklist](#implementation-checklist)
8. [Best Practices](#best-practices)

---

## Visual Design Foundations

### Core Principles

| Principle | Description | Application |
|-----------|-------------|--------------|
| **Clarity** | Every element communicates its purpose | Clear hierarchy, readable typography |
| **Consistency** | Systematic use of tokens and patterns | Reusable components, predictable behavior |
| **Accessibility** | WCAG 2.1 AA compliance by default | Contrast ratios, semantic HTML, keyboard nav |
| **Performance** | Optimized for perceived speed | Lazy loading, skeleton screens, 60fps animations |

### Typography System

**Modular Scale** (1.2 ratio - Minor Third):
```css
:root {
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  --text-5xl: 3rem;        /* 48px */
  --text-6xl: 3.75rem;     /* 60px */
}
```

**Line Height Guidelines**:
- Headings: 1.1 - 1.3
- Body text: 1.5 - 1.7
- UI labels: 1.2 - 1.4

### Color System

**Semantic Token Hierarchy**:
```css
:root {
  /* Primitive → Semantic → Component */
  --color-blue-500: #3b82f6;           /* Primitive */
  --color-primary: var(--color-blue-500); /* Semantic */
  --button-bg: var(--color-primary);      /* Component */
}
```

**WCAG Contrast Requirements**:
| Element | Minimum Ratio | Enhanced (AAA) |
|---------|---------------|-----------------|
| Body text | 4.5:1 | 7:1 |
| Large text (18px+) | 3:1 | 4.5:1 |
| UI components | 3:1 | - |

### Spacing System

**8-point Grid**:
```css
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
}
```

**Component Spacing**:
- Card padding: `--space-4` to `--space-6`
- Section gap: `--space-8` to `--space-16`
- Form field gap: `--space-4` to `--space-6`
- Icon-text gap: `--space-2`

See [references/visual-design/](references/visual-design/) for detailed typography, color systems, and spacing guidelines.

---

## Design Systems

### Token Architecture

**Three-Layer Hierarchy**:

```
Primitive Tokens → Semantic Tokens → Component Tokens
     ↓                  ↓                   ↓
  Raw Values         Contextual          Usage-Specific
  (#3b82f6)        (text-primary)       (button-bg)
```

### Theming Infrastructure

**Theme Provider Pattern** (React):
```tsx
const ThemeContext = createContext<ThemeValue | null>(null);

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState<Theme>("system");

  useEffect(() => {
    const root = document.documentElement;

    const applyTheme = (isDark: boolean) => {
      root.classList.toggle("dark", isDark);
    };

    if (theme === "system") {
      const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
      applyTheme(mediaQuery.matches);

      const handler = (e: MediaQueryListEvent) => applyTheme(e.matches);
      mediaQuery.addEventListener("change", handler);
      return () => mediaQuery.removeEventListener("change", handler);
    } else {
      applyTheme(theme === "dark");
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

### Component Variant System

**CVA Pattern**:
```tsx
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium transition-colors",
  {
    variants: {
      variant: {
        primary: "bg-primary text-primary-foreground hover:bg-primary/90",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        sm: "h-9 px-3 text-sm",
        md: "h-10 px-4",
        lg: "h-11 px-8 text-base",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);
```

See [references/design-systems/](references/design-systems/) for token pipelines, Style Dictionary config, and multi-brand strategies.

---

## Responsive Design

### Modern Breakpoint Scale

```css
/* Mobile-first breakpoints */
@media (min-width: 640px)  { /* sm: Landscape phones, small tablets */ }
@media (min-width: 768px)  { /* md: Tablets */ }
@media (min-width: 1024px) { /* lg: Laptops, small desktops */ }
@media (min-width: 1280px) { /* xl: Desktops */ }
@media (min-width: 1536px) { /* 2xl: Large desktops */ }
```

### Container Queries

```css
/* Define containment context */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query the container, not viewport */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}
```

### Fluid Typography

```css
/* Fluid type scale using clamp() */
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-xl: clamp(1.25rem, 1rem + 1.25vw, 1.5rem);
}
```

### CSS Grid Layouts

```css
/* Auto-fit grid - items wrap automatically */
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: 1.5rem;
}
```

See [references/responsive/](references/responsive/) for container query patterns, fluid layouts, and breakpoint strategies.

---

## Component Design

### Composition Patterns

**Compound Components**:
```tsx
<Select value={value} onChange={setValue}>
  <Select.Trigger>Choose option</Select.Trigger>
  <Select.Options>
    <Select.Option value="a">Option A</Select.Option>
    <Select.Option value="b">Option B</Select.Option>
  </Select.Options>
</Select>
```

**Render Props**:
```tsx
<DataFetcher url="/api/users">
  {({ data, loading, error }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
</DataFetcher>
```

**Slots** (Vue/Svelte):
```vue
<Card>
  <template #header>Title</template>
  <template #content>Body text</template>
  <template #footer><Button>Action</Button></template>
</Card>
```

### CSS-in-JS Approaches

| Solution | Approach | Best For |
|----------|-----------|-----------|
| **Tailwind CSS** | Utility classes | Rapid prototyping, design systems |
| **CSS Modules** | Scoped CSS files | Existing CSS, gradual adoption |
| **styled-components** | Template literals | React, dynamic styling |
| **Vanilla Extract** | Zero-runtime | Performance-critical apps |

### Component API Design

```tsx
interface ButtonProps {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  isDisabled?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}
```

**Principles**:
- Use semantic prop names (`isLoading` vs `loading`)
- Provide sensible defaults
- Support composition via `children`
- Allow style overrides via `className` or `style`

See [references/components/](references/components/) for React, Vue, and Svelte patterns with complete examples.

---

## Interaction Design

### Timing Guidelines

| Duration | Use Case |
|-----------|-----------|
| 100-150ms | Micro-feedback (hovers, clicks) |
| 200-300ms | Small transitions (toggles, dropdowns) |
| 300-500ms | Medium transitions (modals, page changes) |
| 500ms+ | Complex choreographed animations |

### Easing Functions

```css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);   /* Decelerate - entering */
  --ease-in: cubic-bezier(0.55, 0, 1, 0.45);   /* Accelerate - exiting */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1); /* Both - moving between */
  --spring: cubic-bezier(0.34, 1.56, 0.64, 1);   /* Overshoot - playful */
}
```

### Microinteractions

**Hover Lift**:
```css
.hover-lift {
  transition: transform 0.2s var(--ease-out), box-shadow 0.2s var(--ease-out);
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

**Ripple Effect**:
```tsx
function RippleButton({ children, onClick }) {
  const [ripples, setRipples] = useState([]);

  const handleClick = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const ripple = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
      id: Date.now(),
    };
    setRipples((prev) => [...prev, ripple]);
    setTimeout(() => {
      setRipples((prev) => prev.filter((r) => r.id !== ripple.id));
    }, 600);
    onClick?.(e);
  };

  return (
    <button onClick={handleClick} className="relative overflow-hidden">
      {children}
      {ripples.map((ripple) => (
        <span
          key={ripple.id}
          className="absolute bg-white/30 rounded-full animate-ripple"
          style={{ left: ripple.x, top: ripple.y }}
        />
      ))}
    </button>
  );
}
```

### Loading States

**Skeleton Screens**:
```tsx
function CardSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-48 bg-gray-200 rounded-lg" />
      <div className="mt-4 h-4 bg-gray-200 rounded w-3/4" />
      <div className="mt-2 h-4 bg-gray-200 rounded w-1/2" />
    </div>
  );
}
```

See [references/interaction/](references/interaction/) for animation libraries, scroll animations, and gesture patterns.

---

## Mobile Development

### iOS (SwiftUI)

**Stack-Based Layouts**:
```swift
VStack(alignment: .leading, spacing: 12) {
    Text("Title").font(.headline)
    Text("Subtitle").font(.subheadline).foregroundStyle(.secondary)
}
```

**Navigation Stack** (iOS 16+):
```swift
NavigationStack(path: $path) {
    List(items) { item in
        NavigationLink(value: item) {
            ItemRow(item: item)
        }
    }
    .navigationTitle("Items")
    .navigationDestination(for: Item.self) { item in
        ItemDetailView(item: item)
    }
}
```

**SF Symbols**:
```swift
// Variable symbol (iOS 16+)
Image(systemName: "speaker.wave.3.fill", variableValue: volume)

// Symbol effect (iOS 17+)
Image(systemName: "bell.fill")
    .symbolEffect(.bounce, value: notificationCount)
```

### React Native

**StyleSheet Pattern**:
```typescript
const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#ffffff',
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
    color: '#1a1a1a',
  },
});
```

**React Navigation**:
```typescript
const Stack = createNativeStackNavigator<RootStackParamList>();

function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerStyle: { backgroundColor: '#6366f1' } }}>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Detail" component={DetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**Reanimated 3**:
```typescript
const scale = useSharedValue(1);

const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ scale: scale.value }],
}));

const handlePress = () => {
  scale.value = withSpring(1.2, {}, () => {
    scale.value = withSpring(1);
  });
};
```

### Platform-Specific Patterns

**Platform.select()**:
```typescript
const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: {
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 4,
      },
    }),
  },
});
```

See [references/mobile/](references/mobile/) for iOS HIG, Android Material Design, and navigation patterns.

---

## Implementation Checklist

### Pre-Development

- [ ] Define typography scale and font pairings
- [ ] Establish color palette with WCAG compliance
- [ ] Create spacing system (8-point grid)
- [ ] Document icon sizing and usage
- [ ] Choose component composition strategy
- [ ] Select CSS-in-JS solution
- [ ] Plan responsive breakpoints
- [ ] Define animation timing scale

### Component Development

- [ ] Create base tokens (primitives)
- [ ] Define semantic tokens (contextual)
- [ ] Build core components (Button, Input, Card)
- [ ] Implement variant system (CVA or similar)
- [ ] Add compound component patterns
- [ ] Create slot-based composition
- [ ] Document component APIs
- [ ] Cover all states (hover, focus, disabled, error, loading)

### Accessibility Testing

- [ ] Verify color contrast (4.5:1 minimum)
- [ ] Test keyboard navigation (Tab, Enter, Escape)
- [ ] Check focus indicators are visible
- [ ] Validate with screen reader (VoiceOver/NVDA)
- [ ] Ensure touch targets are 44x44px minimum
- [ ] Test with `prefers-reduced-motion`
- [ ] Verify ARIA labels and roles
- [ ] Check form error associations

### Responsive Testing

- [ ] Test on actual devices (not just simulators)
- [ ] Verify container query behavior
- [ ] Check fluid typography scaling
- [ ] Test horizontal scroll scenarios
- [ ] Validate viewport units (dvh, svh, lvh)
- [ ] Check touch interactions on mobile
- [ ] Verify safe area insets on notched devices

### Performance

- [ ] Optimize images (WebP, lazy loading)
- [ ] Subset and optimize fonts
- [ ] Use `transform` and `opacity` for animations
- [ ] Implement skeleton screens
- [ ] Add loading states
- [ ] Minimize layout shifts
- [ ] Profile with Lighthouse
- [ ] Test on low-end devices

---

## Best Practices

### Cross-Domain Principles

1. **Systematic Consistency**
   - Use design tokens religiously
   - Follow naming conventions
   - Document decisions

2. **Accessibility First**
   - WCAG AA minimum, AAA target
   - Semantic HTML
   - Keyboard navigation
   - Screen reader support

3. **Performance by Default**
   - Lazy load images
   - Skeleton screens
   - Efficient animations
   - Optimized assets

4. **Progressive Enhancement**
   - Core content works without JS
   - Enhanced experience for capable browsers
   - Graceful degradation

5. **Mobile-First Thinking**
   - Start with constraints
   - Enhance for larger screens
   - Touch-friendly targets

### Common Anti-Patterns

❌ **Avoid**:
- Hardcoded values (use tokens)
- Multiple primary colors
- Generic gradients (blue/purple)
- Heavy shadows
- Missing states (loading, error, empty)
- Black (#000) text (use dark gray)
- Animating expensive properties (width, height, top)
- Ignoring accessibility

✅ **Prefer**:
- Semantic tokens
- Consistent spacing
- Purposeful motion
- Clear hierarchy
- Generous white space
- Tested components
- Documented patterns

---

## Quick Reference Guides

### Design Token Template
```css
:root {
  /* Spacing */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */

  /* Typography */
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.5rem;

  /* Colors */
  --color-primary: #3b82f6;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;

  /* Effects */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);

  /* Animation */
  --transition-fast: 150ms;
  --transition-base: 250ms;
  --transition-slow: 350ms;
}
```

### Responsive Container
```tsx
function ResponsiveContainer({ children }) {
  return (
    <div className="w-full mx-auto px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {children}
      </div>
    </div>
  );
}
```

### Button Component (React + Tailwind)
```tsx
export function Button({
  variant = "primary",
  size = "md",
  isLoading = false,
  children,
  className,
  ...props
}) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-md font-medium transition-colors",
        "focus-visible:outline-none focus-visible:ring-2",
        "disabled:pointer-events-none disabled:opacity-50",
        {
          "bg-primary text-primary-foreground hover:bg-primary/90": variant === "primary",
          "bg-secondary text-secondary-foreground hover:bg-secondary/80": variant === "secondary",
        },
        {
          "h-9 px-3 text-sm": size === "sm",
          "h-10 px-4": size === "md",
          "h-11 px-8 text-base": size === "lg",
        },
        className
      )}
      disabled={isLoading}
      {...props}
    >
      {isLoading && <Spinner className="mr-2 h-4 w-4" />}
      {children}
    </button>
  );
}
```

---

## Additional Resources

### Design References
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Radix UI Primitives](https://www.radix-ui.com/primitives)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [Material Design 3](https://m3.material.io/)

### Accessibility
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

### Performance
- [Web.dev Performance](https://web.dev/performance/)
- [Core Web Vitals](https://web.dev/vitals/)
- [Image Optimization Guide](https://web.dev/fast/)

### Platform Specific
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Android Material Design](https://m3.material.io/)
- [React Native Documentation](https://reactnative.dev/)
- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)

### Tooling
- [Style Dictionary](https://amzn.github.io/style-dictionary/)
- [Figma Tokens Plugin](https://tokens.studio/)
- [React Navigation](https://reactnavigation.org/)
- [Framer Motion](https://www.framer.com/motion/)

---

## Domain-Specific References

For deep dives into specific domains, see:

- **[Visual Design](references/visual-design/)** - Typography systems, color theory, spacing scales, iconography
- **[Design Systems](references/design-systems/)** - Token architecture, theming infrastructure, component patterns, Style Dictionary
- **[Responsive Design](references/responsive/)** - Container queries, fluid layouts, breakpoint strategies, CSS Grid
- **[Components](references/components/)** - React/Vue/Svelte patterns, composition strategies, styling approaches
- **[Interaction](references/interaction/)** - Animation timing, microinteractions, loading states, gesture handling
- **[Mobile](references/mobile/)** - iOS SwiftUI, Android Material, React Native patterns, navigation
