import pygame
import map
import models.settings as settings
import gui.settingswin as settingswin
import gui.resultwin as resultwin
import gui.controls as controls

LEFT_MOUSE_BUTTON = 0
RIGHT_MOUSE_BUTTON = 2

TRACK_PATH = 0
NEW_SETTINGS = 1
CONTROLS = 2
QUIT = 3
RESTART = 4


class Pathfinder:
    def __init__(self):
        self.settings = None
        self.map = None
        self.window = None
        self.results = None
        self.clicked = False
        self.selection = True
        pygame.init()

    def set_settings(self):
        self.settings = settings.Settings()
        settings_window = settingswin.SettingsWindow(self.settings)
        settings_window.run()

    def display_result_message(self, results):
        result_window = resultwin.ResultWindow(results[0], results[1])
        return result_window.run()

    def run(self):
        while True:
            self.set_settings()
            if self.run_process() == QUIT:
                break

        pygame.quit()

    def run_process(self):
        self.window = pygame.display.set_mode(self.settings.size)
        self.map = map.Map(self.settings)
        self.map.generate(self.window)

        while True:
            action = self.handle_events()
            self.window.fill((0, 0, 0))
            self.map.regenerate(self.window)
            pygame.display.update()
            if action == QUIT:
                return QUIT
            if action == NEW_SETTINGS:
                return RESTART
            elif action == CONTROLS:
                controls.ControlsWindow().run()
            elif action == TRACK_PATH and self.map.settings.show_details:
                option = resultwin.ResultWindow(self.results[0], self.results[1]).run()
                if option == resultwin.NEW_SETTINGS:
                    return RESTART
                elif option == resultwin.QUIT:
                    return QUIT

    def handle_events(self):
        selection = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            if pygame.key.get_pressed()[pygame.K_s]:
                self.map.set_start_point(pygame.mouse.get_pos())
            elif pygame.key.get_pressed()[pygame.K_e]:
                self.map.set_end_point(pygame.mouse.get_pos())
            elif pygame.key.get_pressed()[pygame.K_c]:
                self.map.clear_map()
            elif pygame.key.get_pressed()[pygame.K_t]:
                self.results = self.map.track_path()
                return TRACK_PATH
            elif pygame.key.get_pressed()[pygame.K_n]:
                return NEW_SETTINGS
            elif pygame.key.get_pressed()[pygame.K_i]:
                return CONTROLS
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_button = pygame.mouse.get_pressed()
                if clicked_button[LEFT_MOUSE_BUTTON] or clicked_button[RIGHT_MOUSE_BUTTON]:
                    self.selection = clicked_button[0]
                    pos = pygame.mouse.get_pos()
                    self.map.mark_point((pos[0], pos[1]), self.selection)
                    self.clicked = True
            elif event.type == pygame.MOUSEMOTION and self.clicked:
                pos = pygame.mouse.get_pos()
                self.map.mark_point((pos[0], pos[1]), self.selection)
            else:
                self.clicked = False
