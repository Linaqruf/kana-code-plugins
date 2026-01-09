# Cleanup Examples

Before and after examples demonstrating common cleanup patterns.

## Import Cleanup

### Example 1: Unused Named Imports

**Before:**
```typescript
// src/components/Button.tsx
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import classNames from 'classnames';
import lodash from 'lodash';
import { Button as ShadcnButton } from '@/components/ui/button';
import type { ButtonProps, IconProps, ThemeProps } from '@/types';

export function Button({ children, onClick }: ButtonProps) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <ShadcnButton
      onClick={onClick}
      className={classNames('btn', { hovered: isHovered })}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {children}
    </ShadcnButton>
  );
}
```

**Issues Found:**
- `useEffect` - imported but never used
- `useCallback` - imported but never used
- `useMemo` - imported but never used
- `motion` - imported but never used
- `AnimatePresence` - imported but never used
- `lodash` - imported but never used
- `IconProps` - type imported but never used
- `ThemeProps` - type imported but never used

**After:**
```typescript
// src/components/Button.tsx
import React, { useState } from 'react';
import classNames from 'classnames';
import { Button as ShadcnButton } from '@/components/ui/button';
import type { ButtonProps } from '@/types';

export function Button({ children, onClick }: ButtonProps) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <ShadcnButton
      onClick={onClick}
      className={classNames('btn', { hovered: isHovered })}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {children}
    </ShadcnButton>
  );
}
```

---

### Example 2: Duplicate Imports

**Before:**
```typescript
// src/pages/Dashboard.tsx
import { Card } from '@/components/ui';
import { Button } from '@/components/ui';
import { Input } from '@/components/ui';
import { Modal } from '@/components/ui';
import { Tooltip } from '@/components/ui';
```

**After:**
```typescript
// src/pages/Dashboard.tsx
import { Card, Button, Input, Modal, Tooltip } from '@/components/ui';
```

---

## Dead Code Cleanup

### Example 3: Unreachable Code

**Before:**
```typescript
// src/utils/validation.ts
export function validateEmail(email: string): boolean {
  if (!email) {
    return false;
    console.log('Email is empty');           // Dead code
    trackAnalytics('validation_empty');      // Dead code
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function validatePassword(password: string): ValidationResult {
  if (password.length < 8) {
    throw new Error('Password too short');
    return { valid: false, reason: 'length' }; // Dead code
  }

  return { valid: true };
}
```

**After:**
```typescript
// src/utils/validation.ts
export function validateEmail(email: string): boolean {
  if (!email) {
    return false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function validatePassword(password: string): ValidationResult {
  if (password.length < 8) {
    throw new Error('Password too short');
  }

  return { valid: true };
}
```

---

### Example 4: Unused Functions and Methods

**Before:**
```typescript
// src/services/userService.ts
export class UserService {
  // Used - called from UserController
  async getUser(id: string): Promise<User> {
    return this.db.users.findById(id);
  }

  // Used - called from UserController
  async updateUser(id: string, data: UpdateUserDto): Promise<User> {
    return this.db.users.update(id, data);
  }

  // UNUSED - legacy method, never called
  async getUserLegacy(id: string): Promise<LegacyUser> {
    const user = await this.getUser(id);
    return this.convertToLegacyFormat(user);
  }

  // UNUSED - only called by getUserLegacy (which is unused)
  private convertToLegacyFormat(user: User): LegacyUser {
    return {
      userId: user.id,
      userName: user.name,
      userEmail: user.email,
    };
  }

  // UNUSED - deprecated helper, no callers
  private formatUserForExport(user: User): ExportUser {
    return {
      ...user,
      exportedAt: new Date(),
    };
  }
}
```

**After:**
```typescript
// src/services/userService.ts
export class UserService {
  async getUser(id: string): Promise<User> {
    return this.db.users.findById(id);
  }

  async updateUser(id: string, data: UpdateUserDto): Promise<User> {
    return this.db.users.update(id, data);
  }
}
```

---

### Example 5: Unused Variables

**Before:**
```typescript
// src/components/Dashboard.tsx
export function Dashboard({ data }: DashboardProps) {
  const GRID_SIZE = 12;           // Never used
  const MAX_ITEMS = 100;          // Never used
  const [items, setItems] = useState(data.items);
  const [loading, setLoading] = useState(false);
  let tempValue = null;           // Assigned but never read

  const { total, average, unused } = calculateStats(items);
  //                       ^^^^^^^-- destructured but never used

  useEffect(() => {
    tempValue = 'updated';        // Written but never read
    setLoading(true);
    fetchData().then(() => setLoading(false));
  }, []);

  return (
    <div>
      <p>Total: {total}</p>
      <p>Average: {average}</p>
      {loading && <Spinner />}
    </div>
  );
}
```

**After:**
```typescript
// src/components/Dashboard.tsx
export function Dashboard({ data }: DashboardProps) {
  const [items, setItems] = useState(data.items);
  const [loading, setLoading] = useState(false);

  const { total, average } = calculateStats(items);

  useEffect(() => {
    setLoading(true);
    fetchData().then(() => setLoading(false));
  }, []);

  return (
    <div>
      <p>Total: {total}</p>
      <p>Average: {average}</p>
      {loading && <Spinner />}
    </div>
  );
}
```

---

## Dependency Cleanup

### Example 6: package.json Cleanup

**Before:**
```json
{
  "name": "my-app",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0",
    "lodash": "^4.17.21",
    "moment": "^2.29.4",
    "dayjs": "^1.11.9",
    "classnames": "^2.3.2",
    "clsx": "^2.0.0",
    "@types/node": "^20.4.0",
    "typescript": "^5.1.6"
  },
  "devDependencies": {
    "eslint": "^8.45.0",
    "prettier": "^3.0.0",
    "jest": "^29.6.0"
  }
}
```

**Issues Found:**
- `moment` and `dayjs` - functional duplicates (date libraries)
- `classnames` and `clsx` - functional duplicates (class merging)
- `@types/node` - should be in devDependencies
- `typescript` - should be in devDependencies
- `lodash` - imported 0 times in codebase (unused)

**After:**
```json
{
  "name": "my-app",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0",
    "dayjs": "^1.11.9",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.4.0",
    "typescript": "^5.1.6",
    "eslint": "^8.45.0",
    "prettier": "^3.0.0",
    "jest": "^29.6.0"
  }
}
```

**Changes Summary:**
- Removed `moment` (kept dayjs - smaller)
- Removed `classnames` (kept clsx - smaller)
- Moved `@types/node` to devDependencies
- Moved `typescript` to devDependencies
- Removed unused `lodash`

---

## Config Cleanup

### Example 7: Environment Variables

**Before:**
```bash
# .env
DATABASE_URL=postgres://localhost:5432/app
NEXT_PUBLIC_API_URL=https://api.example.com
SECRET_KEY=abc123

# Unused - old feature removed
LEGACY_API_KEY=old-key-123
FEATURE_OLD_CHECKOUT=false

# Unused - service discontinued
STRIPE_LEGACY_KEY=sk_live_old

# Typo - should be ANALYTICS_ID
ANAYLTICS_ID=GA-12345

# Not documented in .env.example
NEW_FEATURE_FLAG=true
```

**After:**
```bash
# .env
DATABASE_URL=postgres://localhost:5432/app
NEXT_PUBLIC_API_URL=https://api.example.com
SECRET_KEY=abc123
ANALYTICS_ID=GA-12345
NEW_FEATURE_FLAG=true
```

---

### Example 8: Obsolete Config Files

**Before - Directory listing:**
```
project/
├── .babelrc              # Babel not in dependencies
├── .eslintrc.js          # Used
├── .prettierrc           # Used
├── tslint.json           # TSLint is deprecated
├── tsconfig.json         # Used
├── webpack.config.js     # Using Vite now
├── vite.config.ts        # Used
├── .travis.yml           # Migrated to GitHub Actions
└── .github/
    └── workflows/
        └── ci.yml        # Current CI
```

**After - Removed obsolete files:**
```
project/
├── .eslintrc.js
├── .prettierrc
├── tsconfig.json
├── vite.config.ts
└── .github/
    └── workflows/
        └── ci.yml
```

**Removed:**
- `.babelrc` - Vite handles transpilation
- `tslint.json` - TSLint deprecated, use ESLint
- `webpack.config.js` - Migrated to Vite
- `.travis.yml` - Using GitHub Actions

---

## Asset Cleanup

### Example 9: Unused Images

**Before - File structure:**
```
public/
├── images/
│   ├── hero.png           # Used in HomePage
│   ├── logo.png           # Used in Header
│   ├── old-hero.png       # UNUSED - replaced
│   ├── hero-v1.png        # UNUSED - old version
│   ├── hero-v2.png        # UNUSED - old version
│   └── legacy/
│       ├── banner.jpg     # UNUSED - old campaign
│       └── promo.png      # UNUSED - expired promo
├── icons/
│   ├── arrow.svg          # Used
│   ├── check.svg          # Used
│   └── deprecated/
│       ├── old-icon.svg   # UNUSED
│       └── temp.svg       # UNUSED
└── fonts/
    ├── Inter.woff2        # Used in CSS
    ├── OldBrand.woff      # UNUSED - old branding
    └── OldBrand.woff2     # UNUSED - old branding
```

**After - Cleaned:**
```
public/
├── images/
│   ├── hero.png
│   └── logo.png
├── icons/
│   ├── arrow.svg
│   └── check.svg
└── fonts/
    └── Inter.woff2
```

**Savings:** ~850 KB removed

---

## Circular Import Resolution

### Example 10: Breaking Circular Dependencies

**Before - Circular import:**
```typescript
// src/services/userService.ts
import { AuthService } from './authService';  // Imports auth

export class UserService {
  constructor(private auth: AuthService) {}

  async getUser(id: string) {
    if (!this.auth.isAuthenticated()) {
      throw new Error('Not authenticated');
    }
    return this.db.findUser(id);
  }

  async getByEmail(email: string) {
    return this.db.findByEmail(email);
  }
}

// src/services/authService.ts
import { UserService } from './userService';  // Circular!

export class AuthService {
  constructor(private users: UserService) {}

  async login(email: string, password: string) {
    const user = await this.users.getByEmail(email);
    // validate password...
    return this.createSession(user);
  }

  isAuthenticated(): boolean {
    return !!this.session;
  }
}
```

**After - Resolved with interfaces:**
```typescript
// src/services/interfaces.ts (NEW FILE)
export interface IAuthService {
  isAuthenticated(): boolean;
}

export interface IUserService {
  getByEmail(email: string): Promise<User>;
}

// src/services/userService.ts
import type { IAuthService } from './interfaces';

export class UserService implements IUserService {
  constructor(private auth: IAuthService) {}

  async getUser(id: string) {
    if (!this.auth.isAuthenticated()) {
      throw new Error('Not authenticated');
    }
    return this.db.findUser(id);
  }

  async getByEmail(email: string) {
    return this.db.findByEmail(email);
  }
}

// src/services/authService.ts
import type { IUserService } from './interfaces';

export class AuthService implements IAuthService {
  constructor(private users: IUserService) {}

  async login(email: string, password: string) {
    const user = await this.users.getByEmail(email);
    // validate password...
    return this.createSession(user);
  }

  isAuthenticated(): boolean {
    return !!this.session;
  }
}

// src/services/index.ts (composition root)
import { UserService } from './userService';
import { AuthService } from './authService';

// Wire up dependencies
const authService = new AuthService(null as any);  // Temporary
const userService = new UserService(authService);
(authService as any).users = userService;  // Complete circle

export { userService, authService };
```

---

## Full Report Example

```markdown
# Codebase Cleanup Report

Generated: 2024-01-15 10:30:00

## Executive Summary

| Category | Issues Found | Est. Savings |
|----------|--------------|--------------|
| Unused Imports | 23 | - |
| Dead Code | 15 functions | ~500 LOC |
| Unused Assets | 12 files | 2.3 MB |
| Unused Dependencies | 5 packages | 4.1 MB |
| Config Issues | 8 items | - |
| **Total** | **63 issues** | **~6.4 MB** |

## High Priority (Safe to Remove)

### Unused npm Packages
```bash
npm uninstall lodash moment classnames
```

### Unused Asset Files
- `public/images/old-hero.png` (45 KB)
- `public/images/hero-v1.png` (120 KB)
- `public/images/hero-v2.png` (130 KB)
- `public/fonts/OldBrand.woff` (90 KB)
- `public/fonts/OldBrand.woff2` (70 KB)

### Unused Imports (23 files)
See detailed list below...

## Medium Priority (Review Required)

### Potentially Unused Functions (8)
- `src/services/userService.ts`: `getUserLegacy()` - No callers found
- `src/utils/format.ts`: `formatLegacyDate()` - Only test references

### Potentially Unused Exports (5)
- `src/utils/index.ts`: `formatCurrency` - No importers
- `src/types/legacy.ts`: `OldUserType` - No importers

## Low Priority (Manual Review)

### Dynamic Asset Directories
- `public/images/gallery/` (50 files) - Uses dynamic loading
- `src/icons/` (30 SVGs) - Uses require.context

### Feature Flags to Review
- `FEATURE_OLD_CHECKOUT` - Always false for 6+ months
- `ENABLE_LEGACY_API` - No code references found

## Recommended Actions

1. Run: `npm uninstall lodash moment classnames`
2. Delete files in "Unused Asset Files" section
3. Review "Medium Priority" items with team
4. Clean up feature flags in next sprint
```
