from functools import wraps

import wx
from wx.lib.scrolledpanel import ScrolledPanel
from pyxenoverse.gui.ctrl.hex_ctrl import HexCtrl
from pyxenoverse.gui.ctrl.multiple_selection_box import MultipleSelectionBox
from pyxenoverse.gui.ctrl.single_selection_box import SingleSelectionBox
from pyxenoverse.gui.ctrl.single_selection_info_box import SingleSelectionInfoBox
from pyxenoverse.gui.ctrl.unknown_hex_ctrl import UnknownHexCtrl
from pyxenoverse.gui.ctrl.unknown_num_ctrl import UnknownNumCtrl

from yabdm.my_helpers import convert_to_px

MAX_UINT16 = 0xFFFF
MAX_UINT32 = 0xFFFFFFFF


def add_entry(func):
    @wraps(func)
    def entry_wrapper(*args, **kwargs):
        panel, label = args[1], args[2]
        if label:
            panel.sizer.Add(wx.StaticText(panel, -1, label), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP, 10)
            kwargs['name'] = label
        control = func(*args, **kwargs)
        panel.sizer.Add(control, 0, wx.LEFT | wx.TOP, 10)
        return control
    return entry_wrapper


class Page(ScrolledPanel):
    def __init__(self, parent, *args, **kwargs):
        cols = kwargs.pop('cols', 2)
        ScrolledPanel.__init__(self, parent, *args, **kwargs)
        self.sizer = wx.FlexGridSizer(rows=65, cols=cols, hgap=convert_to_px(5), vgap=convert_to_px(5, False))
        self.SetSizer(self.sizer)
        self.SetupScrolling()


class SubEntryPanel(wx.Panel):
    def __init__(self, parent, index):
        wx.Panel.__init__(self, parent)
        self.sub_entry = None
        self.notebook = wx.Notebook(self)
        main_panel = Page(self.notebook)
        animation_panel = Page(self.notebook)
        sound_panel = Page(self.notebook)
        effect_panel = Page(self.notebook)
        pushback_panel = Page(self.notebook)
        camera_panel = Page(self.notebook)
        misc_panel = Page(self.notebook)
        unknown_panel = Page(self.notebook)
        self.notebook.AddPage(main_panel, 'Main')
        self.notebook.AddPage(animation_panel, 'Animation')
        self.notebook.AddPage(sound_panel, 'Sound')
        self.notebook.AddPage(effect_panel, 'Effects')
        self.notebook.AddPage(pushback_panel, 'Pushback/Stun/Knockback')
        self.notebook.AddPage(camera_panel, 'Camera')
        self.notebook.AddPage(misc_panel, 'Misc')
        self.notebook.AddPage(unknown_panel, 'Unknown')

        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 10)

        # Damage
        self.damage_type = self.add_single_selection_info_entry(
            main_panel, 'Damage Type', majorDimension=4, index=index, choices={
                0: ['No effect'],
                1: ['Block'],
                2: ['Guard break'],
                3: ['Standard'],
                4: ['Heavy'],
                5: ['Knockback', {2: 'Fall over', 4: 'Crash bounce', 8: 'Fall over', 9: 'Knockback'}],
                6: ['Knockback', {2: 'Stomach Stun', 4: 'Bounce', 8: 'Stomach stun/Stumble back', 9: 'Stumble back'}],
                7: ['Knockback', {2: 'Arms/legs stretched out', 4: 'Crash Roll', 8: 'Dazed float', 9: 'Knockback'}],
                8: ['Knockback', {2: 'Stomach stun', 4: 'Crash bounce', 8: 'Stomach stun', 9: 'Belly flop'}],
                9: ['Knockback', {2: 'Spin tumble', 4: 'Crash roll bounce', 8: 'Spin tumble', 9: 'Knockback'}],
                10: ['Grab'],
                11: ['Hold stomach', {4: 'Lie down'}],
                12: ['Hold eyes'],
                13: ['Knockback', {2: 'Lie on back', 4: 'Lie on back', 8: 'Lie on back', 9: 'Knockback'}],
                14: ['Electric'],
                15: ['Dazed/asleep'],
                16: ['Paralysis'],
                17: ['Freeze'],
                18: ['Wild-card'],
                19: ['No Effect'],
                20: ['Heavy stamina break', {
                    2: 'Arms/legs stretched out', 4: 'Crash roll', 8: 'Dazed float', 9: 'Knockback'}],
                21: ['Light stamina break', {
                    2: 'Stomach stun', 4: 'Bounce', 8: 'Stomach stun/Stumble back', 9: 'Bounce'}],
                22: ['Giant ki blast push'],
                23: ['Brainwash'],
                24: ['Giant ki blast return'],
                25: ['Knockback', {2: 'Knocked away by head', 4: 'Crash roll', 8: 'Dazed float', 9: 'Knockback'}],
                26: ['Knockback', {2: 'Arms/legs stretched out', 4: 'Crash roll', 8: 'Dazed float', 9: 'Knockback'}],
                27: ['Knockback', {
                    2: 'Back to ground, arms/legs stretched out', 4: 'Crash roll', 8: 'Dazed float', 9: 'Knockback'}],
                28: ['Knockback', {2: 'Arms/legs stretched out', 4: 'Crash roll', 8: 'Dazed float', 9: 'Knockback'}],
                29: ['Slow Opponent'],
                30: ['Brainwash'],
                31: ['Time Stop']
            })
        self.secondary_type = self.add_multiple_selection_entry(
            main_panel, 'Secondary Type', cols=4, orient=wx.VERTICAL, majorDimension=4, choices=[
                ('Damage Orienation', [
                    'Face Opponent Always',
                    'Unknown (0x2)',
                    'Unknown (0x4)',
                    'Unknown (0x8)'], True),
                ('Damage Properties', [
                    'Disable Evasive Usage',
                    'Unknown (0x2)',
                    'Bypass Time Stop Damage',
                    'Bypass Super Armor'], True),
                ('Unknown', None, True),
                ('Health Properties', [
                    'Restore Health'], True)
            ])
        self.damage_amount = self.add_num_entry(main_panel, 'Damage Amount')
        self.damage_special = self.add_num_entry(main_panel, 'Damage Special')
        self.damage_special_2 = self.add_num_entry(main_panel, 'Damage Special 2')

        # Sound
        self.sound_type = self.add_single_selection_entry(sound_panel, 'Sound Type', choices={
            'CAR_BTL_CMN': 0x0,
            'Player SE': 0x2,
            'Player VOX': 0x3,
            'Unknown (0x5)': 0x5,
            'Skill SE': 0xa,
            'Skill VOX': 0xb
        })
        self.sound_id = self.add_num_entry(sound_panel, 'Sound Id')

        # Effect 1
        self.effect_1_eepk_id = self.add_num_entry(effect_panel, 'Effect 1 EEPK Id')
        self.effect_1_skill_id = self.add_num_entry(effect_panel, 'Effect 1 Skill Id')
        self.effect_1_skill_type = self.add_single_selection_entry(effect_panel, 'Effect 1 Skill Type', choices={
            'Global': 0x0,
            'StageBG': 0x1,
            'Player': 0x2,
            'Super': 0x5,
            'Ultimate': 0x6,
            'Evasive': 0x7,
            'Ki Blast': 0x9
        })

        # Effect 2
        self.effect_2_eepk_id = self.add_num_entry(effect_panel, 'Effect 2 EEPK Id')
        self.effect_2_skill_id = self.add_num_entry(effect_panel, 'Effect 2 Skill Id')
        self.effect_2_skill_type = self.add_single_selection_entry(effect_panel, 'Effect 2 Skill Type', choices={
            'Global': 0x0,
            'StageBG': 0x1,
            'Player': 0x2,
            'Super': 0x5,
            'Ultimate': 0x6,
            'Evasive': 0x7,
            'Ki Blast': 0x9
        })

        # Effect 3
        self.effect_3_eepk_id = self.add_num_entry(effect_panel, 'Effect 3 EEPK Id')
        self.effect_3_skill_id = self.add_num_entry(effect_panel, 'Effect 3 Skill Id')
        self.effect_3_skill_type = self.add_single_selection_entry(effect_panel, 'Effect 3 Skill Type', choices={
            'Global': 0x0,
            'StageBG': 0x1,
            'Player': 0x2,
            'Super': 0x5,
            'Ultimate': 0x6,
            'Evasive': 0x7,
            'Ki Blast': 0x9
        })

        # Pushback
        self.pushback_speed = self.add_float_entry(pushback_panel, 'Pushback Speed')
        self.pushback_acceleration_percent = self.add_float_entry(pushback_panel, 'Pushback Acceleration Percent')

        # Stun
        self.user_stun = self.add_num_entry(pushback_panel, 'User Stun')
        self.victim_stun = self.add_num_entry(pushback_panel, 'Victim Stun')

        # Knockback
        self.knockback_duration = self.add_num_entry(pushback_panel, 'Knockback Duration')
        self.knockback_ground_impact_time = self.add_num_entry(pushback_panel, 'Knockback Ground Impact Time')
        self.knockback_recovery_after_impact_time = self.add_num_entry(
            pushback_panel, 'Knockback Recovery\nAfter Impact Time')
        self.knockback_strength_x = self.add_float_entry(pushback_panel, 'Knockback Strength X')
        self.knockback_strength_y = self.add_float_entry(pushback_panel, 'Knockback Strength Y')
        self.knockback_strength_z = self.add_float_entry(pushback_panel, 'Knockback Strength Z')
        self.knockback_drag_y = self.add_float_entry(pushback_panel, 'Knockback Drag Y')
        self.knockback_gravity_time = self.add_num_entry(pushback_panel, 'Knockback Gravity Time')
        self.victim_invincibility_time = self.add_num_entry(pushback_panel, 'Victim Invincibility Time')

        # Misc
        self.transformation_type = self.add_unknown_num_entry(misc_panel, 'Transformation Type', knownValues={
            0: 'None',
            1: 'Candy'
        })
        self.ailment_type  = self.add_multiple_selection_entry(
            misc_panel, 'Ailmemt Type', cols=4, orient=wx.VERTICAL, majorDimension=2, choices=[
                ('Properties #2', [
                    'Seal Awoken skill',
                    'Unknown (0x2)',
                    'Unknown (0x4)',
                    'Unknown (0x8)'], True),
                ('Properties #1', [
                    'Unknown (0x1)',
                    'HP/DEF',
                    'SPD',
                    'Target?'], True)
            ])
        self.stumble_type = self.add_num_entry(misc_panel, 'Stumble Type')

        # Camera
        self.camera_shake_type = self.add_unknown_num_entry(
            camera_panel, 'Camera Shake Type', False, min=-1, knownValues={
                -1: 'None',
                0: 'Rumble',
                1: 'Heavy rumble',
                2: 'Extreme rumble',
                3: 'None',
                4: 'None',
                5: 'None',
                6: 'Camera zoom on impact point',
                7: 'Static camera',
                8: 'Camera focus on victim',
                9: 'None',
                10: 'Camera zoom and focus on victim'
            })
        self.camera_shake_time = self.add_num_entry(camera_panel, 'Camera Shake Time')
        transparent_values = {-1: 'None'}
        transparent_values.update({value: f'{int(value/15.0 * 100)}% Opaque' for value in range(16)})
        self.user_bpe_id = self.add_unknown_num_entry(
            camera_panel, 'User BPE ID', min=-1, max=9999)
        self.opponent_bpe_id = self.add_unknown_num_entry(
            camera_panel, 'Opponent BPE ID', min=-1, max=9999)

        # Stamina/Z Vanish
        self.stamina_broken_bdm_id_override = self.add_num_entry(
            misc_panel, 'Stamina Broken BDM Id Override')
        self.time_before_z_vanish_enabled = self.add_num_entry(
            misc_panel, 'Time Before Z Vanish Enabled')

        # User Animation
        self.user_animation_time = self.add_num_entry(animation_panel, 'User Animation Time')
        self.user_animation_speed = self.add_float_entry(animation_panel, 'User Animation Speed')

        # Victim Animation
        self.victim_animation_time = self.add_num_entry(animation_panel, 'Victim Animation Time')
        self.victim_animation_speed = self.add_float_entry(animation_panel, 'Victim Animation Speed')

        # Unknowns
        self.u_02 = self.add_hex_entry(unknown_panel, 'U_02')
        self.u_06 = self.add_hex_entry(unknown_panel, 'U_06')
        self.f_08 = self.add_float_entry(unknown_panel, 'F_08')
        self.u_16 = self.add_hex_entry(unknown_panel, 'U_16')
        self.u_1e = self.add_hex_entry(unknown_panel, 'U_1E')
        self.u_26 = self.add_hex_entry(unknown_panel, 'U_26')
        self.u_3a = self.add_hex_entry(unknown_panel, 'U_3A')
        self.u_4c = self.add_hex_entry(unknown_panel, 'U_4C')
        self.u_52 = self.add_hex_entry(unknown_panel, 'U_52')
        self.u_58 = self.add_hex_entry(unknown_panel, 'U_58')
        self.u_5a = self.add_hex_entry(unknown_panel, 'U_5A')
        self.u_5c = self.add_hex_entry(unknown_panel, 'U_5C')
        self.u_60 = self.add_hex_entry(unknown_panel, 'U_60')



        # Binds
        self.Bind(wx.EVT_TEXT, self.save_sub_entry)
        self.Bind(wx.EVT_CHECKBOX, self.save_sub_entry)
        self.Bind(wx.EVT_RADIOBOX, self.save_sub_entry)

        # Publisher
        # pub.subscribe(self.focus, 'focus')

        # Layout sizers
        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def __getitem__(self, item):
        return self.__getattribute__(item)

    @add_entry
    def add_hex_entry(self, parent, _, *args, **kwargs):
        return HexCtrl(parent, *args, **kwargs)

    @add_entry
    def add_unknown_hex_entry(self, panel, _, *args, **kwargs):
        return UnknownHexCtrl(panel, *args, **kwargs)

    @add_entry
    def add_num_entry(self, panel, _, unsigned=True, *args, **kwargs):
        if 'min' not in kwargs:
            kwargs['min'] = 0 if unsigned else -32768
        if 'max' not in kwargs:
            kwargs['max'] = 65535 if unsigned else 32767
        return wx.SpinCtrl(panel, *args, **kwargs)

    @add_entry
    def add_unknown_num_entry(self, panel, _, unsigned=True, *args, **kwargs):
        if 'min' not in kwargs:
            kwargs['min'] = 0 if unsigned else -32768
        if 'max' not in kwargs:
            kwargs['max'] = 65535 if unsigned else 32767
        return UnknownNumCtrl(panel, *args, **kwargs)

    @add_entry
    def add_float_entry(self, panel, _, *args, **kwargs):
        if 'min' not in kwargs:
            kwargs['min'] = -3.4028235e38
        if 'max' not in kwargs:
            kwargs['max'] = 3.4028235e38
        
        kwargs['inc'] = 0.01
        return wx.SpinCtrlDouble(panel, *args, **kwargs)

    @add_entry
    def add_multiple_selection_entry(self, panel, _, *args, **kwargs):
        return MultipleSelectionBox(panel, *args, **kwargs)

    @add_entry
    def add_single_selection_entry(self, panel, _, *args, **kwargs):
        return SingleSelectionBox(panel, *args, **kwargs)

    @add_entry
    def add_single_selection_info_entry(self, panel, _, *args, **kwargs):
        return SingleSelectionInfoBox(panel, *args, **kwargs)

    def load_sub_entry(self, sub_entry):
        for name in sub_entry.__fields__:
            self[name.lower()].SetValue(sub_entry[name])
        self.sub_entry = sub_entry

    def save_sub_entry(self, _):
        if not self.sub_entry:
            return
        for name in self.sub_entry.__fields__:
            # SpinCtrlDoubles suck
            control = self[name.lower()]  # MY CHANGE: use lowercase cuz this entry's attrs are in lower case
            if isinstance(control, wx.SpinCtrlDouble):
                try:
                    self.sub_entry[name] = float(control.Children[0].GetValue())
                except ValueError:
                    # Keep old value if its mistyped
                    pass
            else:
                self.sub_entry[name] = control.GetValue()

    def focus(self, entry):
        page = self.notebook.FindPage(self[entry].GetParent())
        self.notebook.ChangeSelection(page)
        self[entry].SetFocus()
