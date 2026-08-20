export function logError(error: unknown): void {
  if (!process.env.EV0_INK_DEBUG_ERRORS) {
    return
  }

  console.error(error)
}
