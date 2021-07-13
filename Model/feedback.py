class GiveFeedback:
    """
    Implement the GiveFeedback class.
    """
    def __init__(self, list):
        """
        Initialize the feedback list.
        """
        self.setup  = list[2]
        self.bswing = list[0]
        self.fswing = list[1]
        
    def get_setup(self):
        """
        Get setup feedback.
        """
        if self.setup == "poor":
            return "Your setup is Poor. Your back is stiff. Your feet need to be a shoulder's width apart."
        elif self.setup == "medium":
            return "Your setup is Medium. Make sure to keep your feet shoulder width apart."
        else:
            return "Your setup is Good. Needs no improvement."

    def get_bswing(self):
        """
        Get backswing feedback.
        """
        if self.bswing == "poor":
            return "Your backswing is Poor. Your arms need to be straight. When you swing, the club should be flush with the ball."
        elif self.bswing == "medium":
            return "Your backswing is Medium. Remember to keep your arms straight."
        else:
            return "Your backswing is Good. Needs no improvement."

    def get_fswing(self):
        """
        Get forward swing feedback.
        """
        if self.fswing == "poor":
            return "Your forward swing is Poor. Keep your head down, eyes on the ball. Don't stop early."
        elif self.fswing == "medium":
            return "Your forward swing is Medium. Don't forget to follow through."
        else:
            return "Your forward swing is Good. Needs no improvement."


# def main():
#     feedback = GiveFeedback(["poor", "medium", "good"])
#     setup = feedback.get_setup()
#     bswing = feedback.get_bswing()
#     fswing = feedback.get_fswing()
#     print(setup)
#     print(bswing)
#     print(fswing)
# if __name__ == "__main__":
#     main()