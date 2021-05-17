PROJECT	= template
TARGETU	= SAMD21G18A
TARGETL	= samd21g18a
PORT	= ttyACM0

OBJS	?= Device_Startup/startup_samd21.o \
		   main.o \
		   usvc_kernel/audio.o \
		   usvc_kernel/defaultSounds.o \
		   usvc_kernel/font8x8.o \
		   usvc_kernel/stepTable.o \
		   usvc_kernel/system.o \
		   usvc_kernel/USB_HID_Boot_Keyboard.o \
		   usvc_kernel/usvcUtils.o \
		   usvc_kernel/usb_supported_devices.o \
		   usvc_kernel/USB_HID_Generic_Gamepad.o \
		   usvc_kernel/vga.o \
		   usvc_kernel/usb_host.o

INCS	?= -I./cmsis/samd21 \
		   -I./cmsis/thirdparty
XCPU 	?= -mcpu=cortex-m0plus

CFLAGS	:= -x c -mthumb -D__$(TARGETU)__ $(INCS) -O3 -ffunction-sections -mlong-calls -Wall $(XCPU) -c -std=gnu99 -MD -MP -MF "Device_Startup/startup_samd21.d" -MT"Device_Startup/startup_samd21.d" -MT"Device_Startup/startup_samd21.o"
LFLAGS 	:= -mthumb -Wl,-Map="$(PROJECT).map" --specs=nano.specs --specs=nosys.specs -Wl,--start-group -Wl,--end-group -L"./Device_Startup" -Wl,--gc-sections $(XCPU) -T$(TARGETL)_flash.ld

BOSSAC	?= ./bin/bossac
PACKAGER ?= ./bin/tools/packager.py
TILESET	?= ./bin/tools/tileset.py
TILEMAP	?= ./bin/tools/tilemap.py
EDITOR	?= ./bin/editor/uChipPlayMapEditor.jar

PYTHON	?= python3
JAVA	?= java

ARMGNU	?= arm-none-eabi-
CC 		:= $(ARMGNU)gcc
LD 		:= $(ARMGNU)gcc
OBJDUMP	:= $(ARMGNU)objdump
OBJCOPY	:= $(ARMGNU)objcopy
SIZE	:= $(ARMGNU)size

all: build

build: $(PROJECT).bin

rebuild: clean $(PROJECT).bin

debug: CFLAGS+=-DDEBUG
debug: clean $(PROJECT).bin bossac

release: CFLAGS+=-DUSE_BOOTLOADER
release: clean $(PROJECT).bin package

$(PROJECT).bin: $(OBJS)
	$(LD) -o $(PROJECT).elf $(OBJS) $(LFLAGS)

	$(OBJCOPY) -O binary $(PROJECT).elf $(PROJECT).bin
	$(OBJCOPY) -O ihex -R .eeprom -R .fuse -R .lock -R .signature  $(PROJECT).elf $(PROJECT).hex
	$(OBJCOPY) -j .eeprom --set-section-flags=.eeprom=alloc,load --change-section-lma .eeprom=0 --no-change-warnings -O binary $(PROJECT).elf $(PROJECT).eep || exit 0
	$(OBJDUMP) -h -S $(PROJECT).elf > $(PROJECT).lss
	$(OBJCOPY) -O srec -R .eeprom -R .fuse -R .lock -R .signature  $(PROJECT).elf $(PROJECT).srec
	$(SIZE) $(PROJECT).elf

	cp $(PROJECT).bin ./release/binary.bin

%.o: %.c
	$(CC) $(CFLAGS) -o $@ $<

bossac:
	$(BOSSAC) -d -i -e -w  -o 0x2000 -R ./release/binary.bin --port=$(PORT)

package:
	$(PYTHON) $(PACKAGER) -d ./release
	cp ./release/game.usc ./release/$(PROJECT).usc

editor:
	$(JAVA) -jar $(EDITOR)

list:
	dmesg | grep -i itaca
	dmesg | grep -i acm

clean:
	rm -rfv *.bin *.o *.elf *.lst *.eep *.lss *.srec Device_Startup/*.o usvc_kernel/*.o
