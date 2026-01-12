export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      ".onrender.com"
    ]
  }
});
