# ---- base ----
FROM node:20-alpine AS base
WORKDIR /app
# Needed by Next.js (sharp) on Alpine
RUN apk add --no-cache libc6-compat
# Make pnpm available in this and all inheriting stages
RUN corepack enable && corepack prepare pnpm@latest --activate

# Allow the API + auth cookie values to be injected at build time so
# the compiled Next.js output calls the right backend when running in Docker.
ARG NEXT_PUBLIC_API_URL="http://localhost:5000/api"
ARG JWT_COOKIE_NAME="retail_token"
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV JWT_COOKIE_NAME=${JWT_COOKIE_NAME}

# ---- deps ----
FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# ---- build ----
FROM base AS build
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# If you use Next.js, this is typically `pnpm build` -> "next build"
RUN pnpm build

# ---- runner ----
FROM base AS runner
ENV NODE_ENV=production
WORKDIR /app
EXPOSE 3000

# minimal runtime copy (adjust if you use Next.js standalone output)
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=deps  /app/node_modules ./node_modules
COPY package.json ./

# If your package.json has "start": "next start"
CMD ["pnpm","start"]



# # deps
# FROM node:20-alpine AS deps
# WORKDIR /app
# COPY package.json pnpm-lock.yaml ./
# RUN corepack enable && pnpm i --frozen-lockfile

# # build
# FROM node:20-alpine AS build
# WORKDIR /app
# COPY --from=deps /app/node_modules ./node_modules
# COPY . .
# RUN pnpm build

# # run
# FROM node:20-alpine AS runner
# WORKDIR /app
# ENV NODE_ENV=production
# EXPOSE 3000
# # copy minimal runtime
# COPY --from=build /app/.next ./.next
# COPY --from=build /app/public ./public
# COPY --from=build /app/package.json ./package.json
# COPY --from=build /app/node_modules ./node_modules
# CMD ["pnpm","start","--","-p","3000","-H","0.0.0.0"]
