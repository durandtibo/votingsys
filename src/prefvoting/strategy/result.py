class MajorityResult:
    def get_winner(self) -> str:
        r"""Get the winner name.

        Returns:
            The winner name.

        Raises:
            RuntimeError: if there is 0 or more than 1 winner.
        """

    def get_winners(self) -> tuple[str, ...]:
        r"""Get the winner names.

        Returns:
            The winner names.
        """

    def get_count(self) -> dict:
        r"""Get the count per candidate."""
