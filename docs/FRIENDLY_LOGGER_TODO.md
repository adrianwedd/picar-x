# Friendly Logger Roadmap

This brief outlines next improvements for the kid-friendly logging system.

1. **Roll out to more demos**
   - Integrate `friendly_log` with `example/4.avoiding_obstacles.py` (announce distance readings and turns).
   - Add playful messages to `example/5.minecart_plus.py` when the car detects the line or loses it.
   - Consider a “quiet” flag for parents who prefer minimal output.

2. **Add file logging for adults**
   - Mirror friendly logs into a simple text file (e.g., `logs/friendly.log`) with timestamps for later review.
   - Ensure file logging is optional so SD cards aren’t filled during long sessions.

3. **Support custom themes**
   - Allow swapping emoji/color sets for different age groups (e.g., animals, space, sports).
   - Document how to pass a color override when calling `friendly_log`.

4. **Provide a testing harness**
   - Write unit tests to verify ANSI codes reset correctly and fallback behaviour when an unknown category is used.
   - Include quick doctest examples in `friendly_logger.py`.

5. **Update documentation**
   - Expand `docs/EXAMPLE_GUIDE.md` with examples showing how to plug the logger into new scripts.
   - Create a short video or GIF showing the colourful terminal output for parents.

Use this roadmap to track enhancements once the initial rollout is validated.
