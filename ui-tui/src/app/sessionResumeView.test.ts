import { afterEach, describe, expect, it, vi } from 'vitest'

const { evictInkCachesMock, forceRedrawMock } = vi.hoisted(() => ({
  evictInkCachesMock: vi.fn(),
  forceRedrawMock: vi.fn()
}))

vi.mock('@3v0/ink', () => ({
  evictInkCaches: evictInkCachesMock,
  forceRedraw: forceRedrawMock
}))

import { refreshSessionView, scheduleResumeScrollToBottom } from './sessionResumeView.js'

describe('refreshSessionView', () => {
  afterEach(() => {
    evictInkCachesMock.mockReset()
    forceRedrawMock.mockReset()
  })

  it('evicts Ink caches and forces a full repaint', () => {
    const stdout = {} as NodeJS.WriteStream

    refreshSessionView(stdout)

    expect(evictInkCachesMock).toHaveBeenCalledWith('all')
    expect(forceRedrawMock).toHaveBeenCalledWith(stdout)
  })
})

describe('scheduleResumeScrollToBottom', () => {
  afterEach(() => {
    vi.useRealTimers()
    evictInkCachesMock.mockReset()
    forceRedrawMock.mockReset()
  })

  it('re-snaps while sticky and stops when the user scrolls away', () => {
    vi.useFakeTimers()
    let sticky = true
    let lastManualScrollAt = 0
    const scrollToBottom = vi.fn()

    const cancel = scheduleResumeScrollToBottom(
      {
        current: {
          getLastManualScrollAt: () => lastManualScrollAt,
          isSticky: () => sticky,
          scrollToBottom
        }
      } as any,
      [0, 80, 240]
    )

    vi.advanceTimersByTime(0)
    expect(scrollToBottom).toHaveBeenCalledTimes(1)
    // The delay-0 tick scrolls only — Ink's normal re-render painted the
    // resumed transcript, so an evict+forceRedraw here would race that frame
    // (the visible resume flash). No force-redraw at 0ms.
    expect(evictInkCachesMock).not.toHaveBeenCalled()
    expect(forceRedrawMock).toHaveBeenCalledTimes(0)

    vi.advanceTimersByTime(80)
    expect(scrollToBottom).toHaveBeenCalledTimes(2)
    // The 80ms sticky-scroll correction DOES force-redraw (correctness).
    expect(forceRedrawMock).toHaveBeenCalledTimes(1)

    sticky = false
    lastManualScrollAt = Date.now() + 1
    vi.advanceTimersByTime(160)
    expect(scrollToBottom).toHaveBeenCalledTimes(2)

    cancel()
  })

  it('cancels pending resume snaps', () => {
    vi.useFakeTimers()
    const scrollToBottom = vi.fn()

    const cancel = scheduleResumeScrollToBottom(
      {
        current: {
          getLastManualScrollAt: () => 0,
          isSticky: () => true,
          scrollToBottom
        }
      } as any,
      [20]
    )

    cancel()
    vi.advanceTimersByTime(20)

    expect(scrollToBottom).not.toHaveBeenCalled()
    expect(forceRedrawMock).not.toHaveBeenCalled()
  })

  it('keeps the immediate resume snap even before sticky state settles', () => {
    vi.useFakeTimers()
    let sticky = false
    const scrollToBottom = vi.fn()

    const cancel = scheduleResumeScrollToBottom(
      {
        current: {
          getLastManualScrollAt: () => 0,
          isSticky: () => sticky,
          scrollToBottom
        }
      } as any,
      [0, 80]
    )

    vi.advanceTimersByTime(0)
    expect(scrollToBottom).toHaveBeenCalledTimes(1)
    // No force-redraw at 0ms — the immediate snap scrolls; the normal
    // re-render paints the content (no mid-frame repaint flash).
    expect(forceRedrawMock).toHaveBeenCalledTimes(0)

    vi.advanceTimersByTime(80)
    expect(scrollToBottom).toHaveBeenCalledTimes(1)
    expect(forceRedrawMock).toHaveBeenCalledTimes(0)

    sticky = true
    cancel()
  })
})
