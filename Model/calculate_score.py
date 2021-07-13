from Model.make_detections_using_model import MakeDetections
from statistics import mean

class EvaluateSwing:

    def __init__(self):
        # ============
        self.all_evals = list() # The most important list here
        # =============

    def process_probabilities(self, folder):

        makeDetections = MakeDetections(folder)
        detections_list = makeDetections.detections

        bk_scores = {'poor':[],'medium':[],'good':[]}
        fw_scores = {'poor':[],'medium':[],'good':[]}   
        st_scores = {'poor':[],'medium':[],'good':[]}

        scores = [bk_scores, fw_scores, st_scores]

        for i in detections_list:

            # Backward swing probabilities
            if "poor_bk" in i[0]:
                bk_scores['poor'].append(i[1])
            elif "medium_bk" in i[0]:
                bk_scores['medium'].append(i[1])
            elif "good_bk" in i[0]:
                bk_scores['good'].append(i[1])

            # Forward swing probabilities
            elif "poor_fw" in i[0]:
                fw_scores['poor'].append(i[1])
            elif "medium_fw" in i[0]:
                fw_scores['medium'].append(i[1])
            elif "good_fw" in i[0]:
                fw_scores['good'].append(i[1])

            # Setup swing probabilities
            elif "poor_st" in i[0]:
                st_scores['poor'].append(i[1])
            elif "medium_st" in i[0]:
                st_scores['medium'].append(i[1])
            elif "good_st" in i[0]:
                st_scores['good'].append(i[1])


        for i in scores:
            if len(i['poor']) > 0:
                poor_count = len(i['poor'])
                poor_weight = mean(i['poor'])
            else:
                poor_count = 0
                poor_weight = 0

            if len(i['medium']) > 0:
                medium_count = len(i['medium'])
                medium_weight = mean(i['medium'])
            else:
                medium_count = 0
                medium_weight = 0

            if len(i['good']) > 0:
                good_count = len(i['good'])
                good_weight = mean(i['good'])
            else:
                good_count = 0
                good_weight = 0
            
            poor_points = (poor_count * poor_weight)
            medium_points = (medium_count * medium_weight)
            good_points = (good_count * good_weight)
            
            points_possible = poor_points + medium_points + good_points
            if points_possible > 0:
                poor_score = poor_points / points_possible
                medium_score = medium_points / points_possible
                good_score = good_points / points_possible
                if medium_score < poor_score > good_score:
                    final_eval = "poor"
                elif poor_score <= medium_score > good_score:
                    final_eval = "medium"
                else:
                    final_eval = "good"
            else: 
                final_eval = "Error"

            self.all_evals.append(final_eval)

        return self.all_evals


# test = EvaluateSwing().process_probabilities('videos/test')
# print(test)