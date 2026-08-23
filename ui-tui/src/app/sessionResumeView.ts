import type { ScrollBoxHandle } from '@3v0/ink'
import { evictInkCaches, forceRedraw } from '@3v0/ink'
import type { RefObject } from 'react'

export const refreshSessionView = (stdout: NodeJS.WriteStream = process.stdout) => {
  evictInkCaches('all')
  forceRedraw(stdout)
}

export const scheduleResumeScrollToBottom = (
  scrollRef: RefObject<null | ScrollBoxHandle>,
  delays: readonly number[] = [0, 80, 240]
) => {
  const startedAt = Date.now()

  const timers = delays.map((delay, index) =>
    setTimeout(() => {
      const scroll = scrollRef.current

      if (!scroll) {
        return
      }

      const manuallyScrolledAfterResume = scroll.getLastManualScrollAt() > startedAt

      if (!manuallyScrolledAfterResume && (index === 0 || scroll.isSticky())) {
        scroll.scrollToBottom()

        // The delay-0 tick scrolls the resumed transcript into place WITHOUT a
        // full force-redraw: Ink's normal re-render has already painted the
        // freshly-set content, and an evict+forceRedraw here races that first
        // frame — the visible full-screen repaint on every resume. The
        // 80/240ms follow-ups still force-redraw (via `refreshSessionView`
        // below) when sticky scroll needs correcting, so correctness holds.
        if (index === 0) {
          return
        }

        refreshSessionView()
      }
    }, delay)
  )

  return () => {
    for (const timer of timers) {
      clearTimeout(timer)
    }
  }
}
