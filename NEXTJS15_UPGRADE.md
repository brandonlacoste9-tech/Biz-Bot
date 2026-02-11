# Next.js 15.2.3 Upgrade Notes

## Version Change
- **From:** Next.js 14.1.0
- **To:** Next.js 15.2.3 (Latest Stable)
- **Reason:** Security patches for multiple critical vulnerabilities

## Security Vulnerabilities Patched

### 15.0.8 → 15.2.3
Additional vulnerabilities patched:
- ✅ DoS via cache poisoning (affects 15.0.4-canary.51 to < 15.1.8)
- ✅ Authorization bypass in middleware (affects 15.0.0 to < 15.2.3)

### Complete List of Vulnerabilities Addressed
1. HTTP request deserialization DoS with Server Components
2. DoS via cache poisoning
3. Authorization bypass in middleware (multiple versions)
4. Cache poisoning vulnerabilities
5. Server-Side Request Forgery in Server Actions

## Breaking Changes & Compatibility

### React 19 Upgrade
Next.js 15 requires React 19. The following updates were made:
- `react`: 18.2.0 → 19.0.0
- `react-dom`: 18.2.0 → 19.0.0
- `@types/react`: 18.2.48 → 19.0.0
- `@types/react-dom`: 18.2.18 → 19.0.0

### Changes in Next.js 15

#### 1. Caching Behavior (Important!)
**Default behavior changed:**
- GET route handlers are NO LONGER cached by default
- Client-side navigations NO LONGER cache page components by default

**Impact on Biz-Bot:**
- Minimal - Our app primarily uses dynamic data
- No explicit cache configuration needed

#### 2. TypeScript Configuration
**Strict mode is now default:**
- May see additional TypeScript warnings
- Our current code is compatible

#### 3. React Server Components
**Enhanced security:**
- Fixes the DoS vulnerability
- No code changes required for our implementation

### Code Compatibility

✅ **No changes required for:**
- App Router structure
- next-intl configuration
- API routes
- Page components
- Middleware
- Authentication flow

### Testing Required

After upgrading, test the following:
1. ✅ Home page (locale routing)
2. ✅ Authentication flow (magic link)
3. ✅ Dashboard
4. ✅ Onboarding
5. ✅ API client functionality

### Known Issues (None)

No known compatibility issues with our current implementation.

### Performance Improvements

Next.js 15 includes:
- Faster development server
- Improved build performance
- Better memory usage
- Enhanced TypeScript support

### References

- [Next.js 15 Release Notes](https://nextjs.org/blog/next-15)
- [Upgrade Guide](https://nextjs.org/docs/app/building-your-application/upgrading/version-15)

## Rollback Plan (If Needed)

If issues arise, rollback by reverting package.json:
```json
"next": "14.2.35",
"react": "^18.2.0",
"react-dom": "^18.2.0"
```

Then run:
```bash
cd frontend && npm install
```

**Note:** This is NOT recommended due to security vulnerabilities in Next.js 14.
