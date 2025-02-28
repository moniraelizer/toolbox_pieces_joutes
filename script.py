import arcpy
from arcpy import da
import os

inTable = arcpy.GetParameterAsText(0)
fileLocation = arcpy.GetParameterAsText(1)

with da.SearchCursor(inTable, ['DATA', 'ATT_NAME', 'ATTACHMENTID']) as cursor:
    for item in cursor:
        attachment = item[0]
        filenum = "ATT" + str(item[2]) + "_"
        filename = filenum + str(item[1])
        open(fileLocation + os.sep + filename, 'wb').write(attachment.tobytes())
        del item
        del filenum
        del filename
        del attachment


## 2nd script 

import arcpy
from arcpy import da
import os
import os.path

# Paramètres d'entrée
inTable = arcpy.GetParameterAsText(0)  # Chemin vers la table en entrée
fileLocation = arcpy.GetParameterAsText(1)  # Dossier de destination pour les fichiers extraits
fieldName = arcpy.GetParameterAsText(2)  # Champ à utiliser comme nom pour les photos
 
try:
    # Vérifie si le dossier de destination existe, sinon le crée
    if not os.path.exists(fileLocation):
        os.makedirs(fileLocation)

    # Parcours de la table avec un SearchCursor
    new_data_name = os.path.basename(inTable)+".DATA"
    new_att_name = os.path.basename(inTable)+".ATT_NAME"
    
    with da.SearchCursor(inTable, [new_data_name, new_att_name, fieldName]) as cursor:
        for item in cursor:
            # Extraction des données de l'attachement
            attachment = item[0]  # Données binaires
            custom_name = str(item[2])  # Valeur du champ spécifié par l'utilisateur
            filename = f"{custom_name}_{item[1]}"  # Construction du nom du fichier
            
            # Crée le chemin complet vers le fichier
            file_path = os.path.join(fileLocation, filename)
            
            # Écrit l'attachement dans un fichier
            with open(file_path, 'wb') as file:
                file.write(attachment.tobytes())
            
            # Message pour informer que le fichier a été sauvegardé
            arcpy.AddMessage(f"Fichier sauvegardé : {file_path}")
except Exception as e:
    # En cas d'erreur, affiche un message d'erreur
    arcpy.AddError(f"Une erreur s'est produite : {e}")