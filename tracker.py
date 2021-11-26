import math

class EuclideanDistTracker:
    def __init__(self):
        # Armazene as posições centrais dos objetos
        self.center_points = {}
        # Contagem de inicio = 1 
        self.id_count = 1

    def update(self, objects_rect):
        # Caixas de objetos e IDs
        objects_bbs_ids = []

        # Obtem o ponto central do novo objeto
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Descubra se esse objeto já foi detectado
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                # Distancia entre um obeto detectado e outro novo
                if dist < 50:
                    self.center_points[id] = (cx, cy)
                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # Novo objeto é detectado, atribuímos o ID a esse objeto
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Limpe o dicionário por pontos centrais para remover IDS que não são mais usados
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Atualizar dicionário com IDs não usados ​​removidos
        self.center_points = new_center_points.copy()
        return objects_bbs_ids