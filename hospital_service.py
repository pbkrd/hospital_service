class Hospital:
    _conditions = {
        0: "Тяжело болен",
        1: "Болен",
        2: "Слегка болен",
        3: "Готов к выписке"
    }

    def __init__(self, start_limit=200):
        self.patients = [Patient() for _ in range(start_limit)]

    def _get_valid_id(self, id):
        if id.isdigit():
            id = int(id) - 1
            if id in range(len(self.patients)):
                return id
            else:
                print("Ошибка. В больнице нет пациента с таким ID")
        else:
            print("Ошибка. ID пациента должно быть числом (целым, положительным)")

    def get_patient_status(self):
        input_id = input("Введите ID пациента: ")
        id = self._get_valid_id(input_id)
        if id is not None:
            patient = self.patients[id]
            print(f"Статус пациента: '{self._conditions[patient.status]}'")

    def patient_status_up(self):
        input_id = input("Введите ID пациента: ")
        id = self._get_valid_id(input_id)
        if id is not None:
            patient = self.patients[id]
            ready_discharge = patient.status_up()
            if ready_discharge:
                may_discharge = input("Желаете этого клиента выписать? (да/нет): ")
                if may_discharge.lower() in ["yes", "да"]:
                    self.discharge_patient(input_id)
                else:
                    print(f"Пациент остался в статусе '{self._conditions[patient.status]}'")
            else:
                print(f"Новый статус пациента: '{self._conditions[patient.status]}'")

    def patient_status_down(self):
        input_id = input("Введите ID пациента: ")
        id = self._get_valid_id(input_id)
        if id is not None:
            patient = self.patients[id]
            error = patient.status_down()
            print(f"Пациент остался в статусе '{self._conditions[patient.status]}'" if error else
                  f"Новый статус пациента: '{self._conditions[patient.status]}'")

    def discharge_patient(self, id=None):
        if id is None:
            id = input("Введите ID пациента: ")
        id = self._get_valid_id(id)
        if id is not None:
            del self.patients[id]
            print("Пациент выписан из больницы")

    def get_stat(self):
        pts, cnds = [*map(int, map(str, self.patients))], self._conditions
        print(f"В больнице на данный момент находится {len(self.patients)} чел., из них:")
        [print(f"- в статусе '{cd}': {pts.count(status)} чел.") for status, cd in cnds.items() if pts.count(status)]


class Patient:
    def __init__(self):
        self.status = 1

    # def __str__(self):
    #     return str(self.status)

    def __repr__(self):
        return str(self.status)

    def status_up(self):
        ready_discharge = self.status == 3
        if ready_discharge:
            return ready_discharge
        self.status += 1

    def status_down(self):
        error = self.status == 0
        if error:
            return error
        self.status -= 1


def main():
    hospital = Hospital()

    ru_eng = {
        "узнать статус пациента": "get status",
        "повысить статус пациента": "status up",
        "понизить статус пациента": "status down",
        "выписать пациента": "discharge",
        "рассчитать статистику": "calculate statistics",

    }
    commands_methods = {
        "get status": hospital.get_patient_status,
        "status up": hospital.patient_status_up,
        "status down": hospital.patient_status_down,
        "discharge": hospital.discharge_patient,
        "calculate statistics": hospital.get_stat
    }

    while True:
        command = input("Введите команду: ").strip().lower()
        if command in ("стоп", "stop"):
            print("Сеанс завершён.")
            print(hospital.patients)
            break
        elif command in ru_eng:
            method = commands_methods[ru_eng[command]]
            method()
        elif command in commands_methods:
            method = commands_methods[command]
            method()
        else:
            print("Неизвестная команда! Попробуйте ещё раз")


if __name__ == "__main__":
    main()
