# Ultimate Frontend Design - Quick Reference

A single-page quick reference for the comprehensive frontend design system.

---

## Domain Selection Guide

| When you need to... | Use this domain |
|---------------------|-----------------|
| Establish design tokens, typography, colors | [Visual Design](#visual-design-quick-reference) |
| Build scalable component libraries | [Design Systems](#design-systems-quick-reference) |
| Create adaptive, fluid layouts | [Responsive Design](#responsive-design-quick-reference) |
| Design reusable components | [Component Design](#component-design-quick-reference) |
| Add animations and microinteractions | [Interaction Design](#interaction-design-quick-reference) |
| Build iOS/Android/React Native apps | [Mobile Development](#mobile-development-quick-reference) |

---

## Visual Design Quick Reference

### Typography Scale

```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.5rem;      /* 24px */
--text-2xl: 2rem;       /* 32px */
```

### Line Heights

- Headings: 1.1 - 1.3
- Body text: 1.5 - 1.7
- UI labels: 1.2 - 1.4

### Spacing System (8-point grid)

```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;      /* 48px */
```

### WCAG Contrast Ratios

| Element | Minimum (AA) | Enhanced (AAA) |
|---------|---------------|-----------------|
| Body text | 4.5:1 | 7:1 |
| Large text (18px+) | 3:1 | 4.5:1 |

---

## Design Systems Quick Reference

### Token Hierarchy

```
Primitive → Semantic → Component
#3b82f6  →  text-primary  →  button-bg
```

### Theme Provider Pattern

```tsx
const ThemeContext = createContext<ThemeValue | null>(null);

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState<Theme>("system");

  useEffect(() => {
    const root = document.documentElement;
    const applyTheme = (isDark: boolean) => {
      root.classList.toggle("dark", isDark);
    };
    // Apply theme based on state or system preference
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

### Component Variants (CVA)

```tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md",
  {
    variants: {
      variant: {
        primary: "bg-primary text-primary-foreground",
        secondary: "bg-secondary text-secondary-foreground",
        ghost: "hover:bg-accent",
      },
      size: {
        sm: "h-9 px-3 text-sm",
        md: "h-10 px-4",
        lg: "h-11 px-8 text-base",
      },
    },
  }
);
```

---

## Responsive Design Quick Reference

### Breakpoints (Mobile-First)

```css
@media (min-width: 640px)  { /* sm */ }
@media (min-width: 768px)  { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

### Container Queries

```css
.container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .child {
    /* Styles when container is 400px+ */
  }
}
```

### Fluid Typography

```css
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 3.5rem);
}
```

### CSS Grid Auto-Fit

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: 1.5rem;
}
```

---

## Component Design Quick Reference

### Composition Patterns

**Compound Components**:
```tsx
<Select>
  <Select.Trigger />
  <Select.Options>
    <Select.Option />
  </Select.Options>
</Select>
```

**Render Props**:
```tsx
<DataFetcher url="/api/users">
  {({ data, loading }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
</DataFetcher>
```

**Slots** (Vue):
```vue
<Card>
  <template #header>Title</template>
  <template #content>Body</template>
</Card>
```

### CSS-in-JS Comparison

| Solution | Best For |
|----------|-----------|
| Tailwind CSS | Rapid prototyping, design systems |
| CSS Modules | Existing CSS, gradual adoption |
| styled-components | React, dynamic styling |
| Vanilla Extract | Performance-critical apps |

### Component API Principles

- Use semantic props (`isLoading` vs `loading`)
- Provide sensible defaults
- Support composition via `children`
- Allow overrides via `className`

---

## Interaction Design Quick Reference

### Animation Timing

| Duration | Use Case |
|----------|-----------|
| 100-150ms | Micro-feedback (hovers, clicks) |
| 200-300ms | Small transitions (toggles) |
| 300-500ms | Medium transitions (modals) |
| 500ms+ | Complex choreographed animations |

### Easing Functions

```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);   /* Entering */
--ease-in: cubic-bezier(0.55, 0, 1, 0.45);   /* Exiting */
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1); /* Moving between */
--spring: cubic-bezier(0.34, 1.56, 0.64, 1);   /* Playful */
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

**Loading Skeleton**:
```tsx
function Skeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-4 bg-gray-200 rounded" />
    </div>
  );
}
```

### Respect Motion Preferences

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Mobile Development Quick Reference

### iOS (SwiftUI)

**Stack Layout**:
```swift
VStack(alignment: .leading, spacing: 12) {
    Text("Title").font(.headline)
    Text("Subtitle").font(.subheadline)
}
```

**Navigation** (iOS 16+):
```swift
NavigationStack(path: $path) {
    List(items) { item in
        NavigationLink(value: item) { ItemRow(item: item) }
    }
    .navigationDestination(for: Item.self) { item in
        ItemDetailView(item: item)
    }
}
```

**SF Symbols**:
```swift
Image(systemName: "star.fill")
Image(systemName: "speaker.wave.3.fill", variableValue: volume)
```

### React Native

**StyleSheet**:
```typescript
const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
});
```

**Navigation**:
```typescript
const Stack = createNativeStackNavigator();

function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
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
```

### Platform-Specific

```typescript
import { Platform } from "react-native";

const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: { shadowColor: "#000", shadowOpacity: 0.1 },
      android: { elevation: 4 },
    }),
  },
});
```

---

## Common Patterns

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
        "inline-flex items-center justify-center rounded-md font-medium",
        "focus-visible:outline-none focus-visible:ring-2",
        "disabled:opacity-50",
        {
          "bg-primary text-white": variant === "primary",
          "bg-secondary text-gray-900": variant === "secondary",
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

### Card Component

```tsx
export function Card({ children, className }) {
  return (
    <div className={cn(
      "bg-white rounded-lg shadow-md p-6",
      "hover:shadow-lg transition-shadow duration-200",
      className
    )}>
      {children}
    </div>
  );
}
```

### Input Component

```tsx
export function Input({
  label,
  error,
  className,
  ...props
}) {
  return (
    <div className="mb-4">
      {label && (
        <label className="block text-sm font-medium mb-2">
          {label}
        </label>
      )}
      <input
        className={cn(
          "w-full px-3 py-2 border rounded-md",
          "focus:outline-none focus:ring-2 focus:ring-primary",
          error && "border-red-500",
          className
        )}
        {...props}
      />
      {error && (
        <p className="text-sm text-red-500 mt-1">{error}</p>
      )}
    </div>
  );
}
```

---

## Implementation Checklist

### Pre-Development
- [ ] Define typography scale
- [ ] Establish color palette (WCAG compliant)
- [ ] Create spacing system
- [ ] Choose component strategy
- [ ] Plan responsive breakpoints
- [ ] Define animation timing

### Component Development
- [ ] Create base tokens
- [ ] Build core components
- [ ] Implement variant system
- [ ] Add compound patterns
- [ ] Document APIs
- [ ] Cover all states

### Testing
- [ ] Color contrast (4.5:1 minimum)
- [ ] Keyboard navigation
- [ ] Focus indicators
- [ ] Screen reader support
- [ ] Touch targets (44x44px min)
- [ ] Reduced motion support
- [ ] Responsive on real devices

### Performance
- [ ] Optimize images (WebP, lazy loading)
- [ ] Subset fonts
- [ ] Use transform/opacity for animations
- [ ] Implement skeleton screens
- [ ] Minimize layout shifts
- [ ] Profile with Lighthouse

---

## Best Practices Summary

### Do's ✅
- Use design tokens consistently
- Maintain WCAG AA compliance
- Start mobile-first
- Use semantic HTML
- Test on real devices
- Provide loading states
- Handle errors gracefully
- Respect motion preferences

### Don'ts ❌
- Hardcode values (use tokens)
- Use multiple primary colors
- Ignore accessibility
- Animate expensive properties (width, height, top)
- Skip testing on devices
- Forget loading/error states
- Use black (#000) for text
- Over-animate

---

## Resources by Domain

### Visual Design
- [Type Scale Calculator](https://typescale.com/)
- [Coolors Palette Generator](https://coolors.co/)
- [Contrast Checker](https://webaim.org/resources/contrastchecker/)

### Design Systems
- [Style Dictionary](https://amzn.github.io/style-dictionary/)
- [Tokens Studio for Figma](https://tokens.studio/)
- [Design Tokens W3C Spec](https://design-tokens.github.io/community-group/format/)

### Responsive Design
- [Every Layout](https://every-layout.dev/)
- [Container Queries Guide](https://web.dev/css-container-queries/)
- [Responsive Images](https://web.dev/responsive-images/)

### Components
- [Radix UI Primitives](https://www.radix-ui.com/primitives)
- [shadcn/ui](https://ui.shadcn.com/)
- [Headless UI](https://headlessui.com/)

### Interaction
- [Framer Motion](https://www.framer.com/motion/)
- [GSAP Animation](https://greensock.com/gsap/)
- [Motion One](https://motion.dev/)

### Mobile
- [iOS HIG](https://developer.apple.com/design/human-interface-guidelines/)
- [Material Design 3](https://m3.material.io/)
- [React Native](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)

---

## Full Documentation

For comprehensive documentation on each domain, see the main [SKILL.md](SKILL.md) file.

Domain-specific deep dives are available in the `references/` directory:
- `references/visual-design/` - Typography, color, spacing, iconography
- `references/design-systems/` - Tokens, theming, component architecture
- `references/responsive/` - Container queries, fluid layouts, breakpoints
- `references/components/` - React/Vue/Svelte patterns
- `references/interaction/` - Animations, microinteractions
- `references/mobile/` - iOS, Android, React Native patterns
