FROM cypress/included:13.13.0
WORKDIR /e2e
COPY cypress/package.json cypress/package-lock.json ./
RUN npm ci
COPY cypress ./
CMD ["npx","cypress","run","--browser","chrome"]
