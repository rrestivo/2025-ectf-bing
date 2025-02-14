/**
 * @file    decoder.c
 * @author  Samuel Meyers
 * @brief   eCTF Decoder Example Design Implementation
 * @date    2025
 *
 * This source file is part of an example system for MITRE's 2025 Embedded System CTF (eCTF).
 * This code is being provided only for educational purposes for the 2025 MITRE eCTF competition,
 * and may not meet MITRE standards for quality. Use this code at your own risk!
 *
 * @copyright Copyright (c) 2025 The MITRE Corporation
 */

/*********************** INCLUDES *************************/
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "mxc_device.h"
#include "status_led.h"
#include "board.h"
#include "mxc_delay.h"
#include "simple_flash.h"
#include "host_messaging.h"
#include <stdlib.h>

#include "simple_uart.h"

/* Code between this #ifdef and the subsequent #endif will
*  be ignored by the compiler if CRYPTO_EXAMPLE is not set in
*  the projectk.mk file. */
#ifdef CRYPTO_EXAMPLE
/* The simple crypto example included with the reference design is intended
*  to be an example of how you *may* use cryptography in your design. You
*  are not limited nor required to use this interface in your design. It is
*  recommended for newer teams to start by only using the simple crypto
*  library until they have a working design. */
#include "simple_crypto.h"
#endif  //CRYPTO_EXAMPLE

/**********************************************************
 ******************* PRIMITIVE TYPES **********************
 **********************************************************/

#define timestamp_t uint64_t
#define channel_id_t uint32_t
#define decoder_id_t uint32_t
#define pkt_len_t uint16_t

/**********************************************************
 *********************** CONSTANTS ************************
 **********************************************************/

#define MAX_CHANNEL_COUNT 8
#define EMERGENCY_CHANNEL 0
#define FRAME_SIZE 64
#define DEFAULT_CHANNEL_TIMESTAMP 0xFFFFFFFFFFFFFFFF
// This is a canary value so we can confirm whether this decoder has booted before
#define FLASH_FIRST_BOOT 0xDEADBEEF

/**********************************************************
 ********************* STATE MACROS ***********************
 **********************************************************/

// Calculate the flash address where we will store channel info as the 2nd to last page available
#define FLASH_STATUS_ADDR ((MXC_FLASH_MEM_BASE + MXC_FLASH_MEM_SIZE) - (2 * MXC_FLASH_PAGE_SIZE))


/**********************************************************
 *********** COMMUNICATION PACKET DEFINITIONS *************
 **********************************************************/

#pragma pack(push, 1) // Tells the compiler not to pad the struct members
// for more information on what struct padding does, see:
// https://www.gnu.org/software/c-intro-and-ref/manual/html_node/Structure-Layout.html
typedef struct {
    channel_id_t channel;
    timestamp_t timestamp;
    uint8_t data[FRAME_SIZE];
} frame_packet_t;

typedef struct {
    decoder_id_t decoder_id;
    timestamp_t start_timestamp;
    timestamp_t end_timestamp;
    channel_id_t channel;
} subscription_update_packet_t;

typedef struct {
    channel_id_t channel;
    timestamp_t start;
    timestamp_t end;
} channel_info_t;

typedef struct {
    uint32_t n_channels;
    channel_info_t channel_info[MAX_CHANNEL_COUNT];
} list_response_t;

#pragma pack(pop) // Tells the compiler to resume padding struct members

/**********************************************************
 ******************** TYPE DEFINITIONS ********************
 **********************************************************/

typedef struct {
    bool active;
    channel_id_t id;
    timestamp_t start_timestamp;
    timestamp_t end_timestamp;
} channel_status_t;

typedef struct {
    uint32_t first_boot; // if set to FLASH_FIRST_BOOT, device has booted before.
    channel_status_t subscribed_channels[MAX_CHANNEL_COUNT];
} flash_entry_t;

/**********************************************************
 ************************ GLOBALS *************************
 **********************************************************/

// This is used to track decoder subscriptions
flash_entry_t decoder_status;

/**********************************************************
 ******************** REFERENCE FLAG **********************
 **********************************************************/

// trust me, it's easier to get the boot reference flag by
// getting this running than to try to untangle this
// TODO: remove this from your final design
// NOTE: you're not allowed to do this in your code
// typedef uint32_t aErjfkdfru;const aErjfkdfru aseiFuengleR[]={0x1ffe4b6,0x3098ac,0x2f56101,0x11a38bb,0x485124,0x11644a7,0x3c74e8,0x3c74e8,0x2f56101,0x2ca498,0x127bc,0x2e590b1,0x1d467da,0x1fbf0a2,0x11a38bb,0x2b22bad,0x2e590b1,0x1ffe4b6,0x2b61fc1,0x1fbf0a2,0x1fbf0a2,0x2e590b1,0x11644a7,0x2e590b1,0x1cc7fb2,0x1d073c6,0x2179d2e,0};const aErjfkdfru djFIehjkklIH[]={0x138e798,0x2cdbb14,0x1f9f376,0x23bcfda,0x1d90544,0x1cad2d2,0x860e2c,0x860e2c,0x1f9f376,0x25cbe0c,0x11c82b4,0x35ff56,0x3935040,0xc7ea90,0x23bcfda,0x1ae6dee,0x35ff56,0x138e798,0x21f6af6,0xc7ea90,0xc7ea90,0x35ff56,0x1cad2d2,0x35ff56,0x2b15630,0x3225338,0x4431c8,0};typedef int skerufjp;skerufjp siNfidpL(skerufjp verLKUDSfj){aErjfkdfru ubkerpYBd=12+1;skerufjp xUrenrkldxpxx=2253667944%0x432a1f32;aErjfkdfru UfejrlcpD=1361423303;verLKUDSfj=(verLKUDSfj+0x12345678)%60466176;while(xUrenrkldxpxx--!=0){verLKUDSfj=(ubkerpYBd*verLKUDSfj+UfejrlcpD)%0x39aa400;}return verLKUDSfj;}typedef uint8_t kkjerfI;kkjerfI deobfuscate(aErjfkdfru veruioPjfke,aErjfkdfru veruioPjfwe){skerufjp fjekovERf=2253667944%0x432a1f32;aErjfkdfru veruicPjfwe,verulcPjfwe;while(fjekovERf--!=0){veruioPjfwe=(veruioPjfwe-siNfidpL(veruioPjfke))%0x39aa400;veruioPjfke=(veruioPjfke-siNfidpL(veruioPjfwe))%60466176;}veruicPjfwe=(veruioPjfke+0x39aa400)%60466176;verulcPjfwe=(veruioPjfwe+60466176)%0x39aa400;return veruicPjfwe*60466176+verulcPjfwe-89;}


/**********************************************************
 ******************* UTILITY FUNCTIONS ********************
 **********************************************************/

/** @brief Checks whether the decoder is subscribed to a given channel
 *
 *  @param channel The channel number to be checked.
 *  @return 1 if the the decoder is subscribed to the channel.  0 if not.
*/
int is_subscribed(channel_id_t channel, timestamp_t timestamp) {
    // Check if this is an emergency broadcast message
    if (channel == EMERGENCY_CHANNEL) {
        return 1;
    }
    // Check if the decoder has has a subscription - > might be off by one error -> make sure it is not checking for channel 9
    for (int i = 0; i < MAX_CHANNEL_COUNT; i++) {

        // retrieves the start and end date of subscribtions for each channel
        // i.e. channel 1 start 1 end 100 -> time starts in boot and counts up
        uint64_t start = decoder_status.subscribed_channels[i].start_timestamp;
        uint64_t end = decoder_status.subscribed_channels[i].end_timestamp;
        // checks if entries in the 
        if ((decoder_status.subscribed_channels[i].id == channel && decoder_status.subscribed_channels[i].active) && ((timestamp <= end)) && (timestamp >= start)) {
        
            return 1;
        }
    }
    return 0;
}

// /** @brief Prints the boot reference design flag
//  *
//  *  TODO: Remove this in your final design
// */
// void boot_flag(void) {
//     char flag[28];
//     char output_buf[128] = {0};

//     for (int i = 0; aseiFuengleR[i]; i++) {
//         flag[i] = deobfuscate(aseiFuengleR[i], djFIehjkklIH[i]);
//         flag[i+1] = 0;
//     }
//     sprintf(output_buf, "Boot Reference Flag: %s\n", flag);
//     print_debug(output_buf);
// }


/**********************************************************
 ********************* CORE FUNCTIONS *********************
 **********************************************************/

/** @brief Lists out the actively subscribed channels over UART.
 *
 *  @return 0 if successful.
*/
int list_channels() {
    list_response_t resp;
    pkt_len_t len;

    resp.n_channels = 0;

    for (uint32_t i = 0; i < MAX_CHANNEL_COUNT; i++) {
        if (decoder_status.subscribed_channels[i].active) {
            resp.channel_info[resp.n_channels].channel =  decoder_status.subscribed_channels[i].id;
            resp.channel_info[resp.n_channels].start = decoder_status.subscribed_channels[i].start_timestamp;
            resp.channel_info[resp.n_channels].end = decoder_status.subscribed_channels[i].end_timestamp;
            resp.n_channels++;
        }
    }

    len = sizeof(resp.n_channels) + (sizeof(channel_info_t) * resp.n_channels);

    // Success message
    write_packet(LIST_MSG, &resp, len);
    return 0;
}


/** @brief Updates the channel subscription for a subset of channels.
 *
 *  @param pkt_len The length of the incoming packet
 *  @param update A pointer to an array of channel_update structs,
 *      which contains the channel number, start, and end timestamps
 *      for each channel being updated.
 *
 *  @note Take care to note that this system is little endian.
 *
 *  @return 0 upon success.  -1 if error.
*/
int update_subscription(pkt_len_t pkt_len, subscription_update_packet_t *update) {
    int i;

    if (update->channel == EMERGENCY_CHANNEL) {
        STATUS_LED_RED();
        print_error("Failed to update subscription - cannot subscribe to emergency channel\n");
        return -1;
    }

    // Find the first empty slot in the subscription array
    for (i = 0; i < MAX_CHANNEL_COUNT; i++) {
        if (decoder_status.subscribed_channels[i].id == update->channel || !decoder_status.subscribed_channels[i].active) {
            decoder_status.subscribed_channels[i].active = true;
            decoder_status.subscribed_channels[i].id = update->channel;
            decoder_status.subscribed_channels[i].start_timestamp = update->start_timestamp;
            decoder_status.subscribed_channels[i].end_timestamp = update->end_timestamp;
            break;
        }
    }

    // If we do not have any room for more subscriptions
    if (i == MAX_CHANNEL_COUNT) {
        STATUS_LED_RED();
        print_error("Failed to update subscription - max subscriptions installed\n");
        return -1;
    }

    flash_simple_erase_page(FLASH_STATUS_ADDR);
    flash_simple_write(FLASH_STATUS_ADDR, &decoder_status, sizeof(flash_entry_t));
    // Success message with an empty body
    write_packet(SUBSCRIBE_MSG, NULL, 0);
    return 0;
}



/**
 * @brief Reads encryption key from a file.
 * 
 * @note HEAP USED HERE check for UAF
 * 
 * @return A pointer to the key if successful, NULL if failed.
 */
// uint8_t* read_key_from_file() {
//     FILE *file = fopen("/global.secrets", "r");
//     if (file == NULL) {
//         perror("Failed to open file");
//         return NULL;
//     }

//     fseek(file, 0, SEEK_END);
//     long fsize = ftell(file);
//     fseek(file, 0, SEEK_SET);

//     char *buffer = malloc(fsize + 1);
//     if (buffer == NULL) {
//         fprintf(stderr, "Memory allocation failed\n");
//         fclose(file);
//         return NULL;
//     }

//     fread(buffer, 1, fsize, file);
//     buffer[fsize] = '\0';
//     fclose(file);

//     char *key_start = strstr(buffer, "\"some_secrets\": \"");
//     if (key_start == NULL) {
//         fprintf(stderr, "Key not found\n");
//         free(buffer);
//         return NULL;
//     }

//     key_start += strlen("\"some_secrets\": \"");
//     uint8_t *key = malloc(KEY_SIZE + 1);
//     if (key == NULL) {
//         fprintf(stderr, "Memory allocation failed for key\n");
//         free(buffer);
//         return NULL;
//     }

//     strncpy((char *)key, key_start, KEY_SIZE);
//     key[KEY_SIZE] = '\0';

//     free(buffer);
//     buffer = NULL;
//     return key;
// }






/**
 * @brief Processes a packet containing frame data.
 *
 * @param pkt_len Length of the incoming packet.
 * @param new_frame A pointer to the incoming packet.
 *
 * @return 0 if successful, -1 if data is from unsubscribed channel.
 */
int decode(pkt_len_t pkt_len, uint8_t* new_frame) {
    uint8_t decrypted_frame[100]; // Buffer to hold the decrypted frame
    uint8_t decrypted_message[FRAME_SIZE];           // Buffer to hold the decrypted message
    char output_buf[128] = {0};
    
    
    /********************************** DEBUG *****************************************************/
    char debug_buf[128] = {0};
    // Debug: Received packet length
    sprintf(debug_buf, "Received Packet Length: %d bytes", pkt_len);
    print_debug(debug_buf);
    /********************************** DEBUG END*****************************************************/
    memset(debug_buf, 0, sizeof(debug_buf));
    memcpy(debug_buf, (char *)new_frame, 80);
    print_debug("PRINT MSG BYTES---->");
    print_hex_debug(debug_buf, 80);





    /********************************** KEY READ *****************************************************/
    // Hardcoded JSON data with the new secret key
    const char* json_data = "{\"channels\": [0, 1, 2, 3, 4, 5, 6, 7, 8], \"some_secrets\": \"a4359d15b2e12213ca1fb8a22efcac31\"}";
    const char* key_start = strstr(json_data, "\"some_secrets\": \"");

    if (key_start == NULL) {
        STATUS_LED_YELLOW();
        print_debug("Key not found in hardcoded JSON");
        return -1;
    }

    // read until key start then moves pointer length of keystart in bytes to start of the key 
    // Move the pointer to the start of the key value
    key_start += strlen("\"some_secrets\": \"");

    // Convert hex key to binary
    uint8_t key[] = {0xa4, 0x35, 0x9d, 0x15, 0xb2, 0xe1, 0x22, 0x13, 0xca, 0x1f, 0xb8, 0xa2, 0x2e, 0xfc, 0xac, 0x31}; // 128-bit key (AES key size typically)
    char key_hex[33]; // Temporary buffer for the key hex string
    strncpy(key_hex, key_start, 32); // Copy hex string to local variable
    key_hex[32] = '\0'; // Null-terminate string

    // Convert hex string to binary
    //for (int i = 0; i < 16; i++) {
    //    sscanf(key_hex + 2 * i, "%2hhx", &key[i]);
    //}

    sprintf(debug_buf, "Encryption Key: %s", key_hex);
    print_debug(debug_buf);

    STATUS_LED_PURPLE();
    print_debug("Key in hex: "); 
    print_hex_debug(key, 16);
    print_debug("------ Key successfully read ------");
    /********************************** KEY READ END *****************************************************/


    ///////////////////////////// FIRST DECRYPT //////////////////////////////////////////////////////////////////////////////
    print_debug("------ Entering decrypt_sym function ------");
    int dec_ret = decrypt_sym(new_frame, pkt_len, key, decrypted_frame);
    if(dec_ret == -1)print_debug("__________PACKET LENGTH ERROR________________");

    if (dec_ret != 0) {
        print_debug("--------------- Failed to decrypt frame ---------------------------");
        return -1; 
    }

    print_debug("------ Leaving decrypt_sym function ------");

    // Print the first 12 bytes as hex
    char header_hex[25];  // Enough space for 12 bytes * 2 chars/byte + 1 null terminator
    for (int i = 0; i < 12; i++) {
        sprintf(&header_hex[i], "%02x", decrypted_frame[i]);
    }
    sprintf(debug_buf, "Decrypted Header: %s", header_hex);
    print_debug(debug_buf);




    frame_packet_t *decrypted_packet = (frame_packet_t *)decrypted_frame;
    memcpy(decrypted_message, decrypted_packet->data, sizeof(decrypted_packet->data));
    uint16_t frame_size = pkt_len - (sizeof(decrypted_packet->channel) + sizeof(decrypted_packet->timestamp));



    /********************************CHECK IF ENCRYPTION SUCCESSFUL************************************************ */
    sprintf(debug_buf, "channel ->  %i timestamp -> %llu", decrypted_packet->channel, decrypted_packet->timestamp);
    print_debug(debug_buf);




    /******************************** DEBUG AFTER decrypt 1 BEFORE decrypt 2************************************************ */
    print_debug("Data copied to decrypted_message.");
    sprintf(debug_buf, "Trimed Frame Size: %d bytes", sizeof(decrypted_packet->data));
    print_debug(debug_buf);
    // Debug: Check alignment issue
    if (sizeof(decrypted_packet->data) % 16 != 0) {
        print_debug("FRAME PACKET NOT DIV BY 16 ERROR!!!!");
    }

    if (sizeof(frame_packet_t) == 0) {
        print_debug("----------------- Frame is empty error ----------------------!!!!");
    }
    /********************************  END DEBUG AFTER decrypt 1 BEFORE decrypt 2************************************************ */
    //  Check subscription validity
    if (is_subscribed(decrypted_packet->channel, decrypted_packet->timestamp)) {
        print_debug("------ Valid Subscription Detected ------");
        ////////////////////////// SECOND DECRYPT ////////////////////////////////////////////////////////////////////////////////////////
        if (decrypt_sym(decrypted_packet->data, FRAME_SIZE, key, decrypted_message) != 0) {
            print_debug("Failed to decrypt message");
            return -1;
        }

        write_packet(DECODE_MSG, decrypted_message, frame_size);
        return 0;
    } else {
        STATUS_LED_RED();
        sprintf(output_buf, "Receiving unsubscribed channel data. Channel: %u", decrypted_packet->channel);
        print_debug(output_buf);
        return -1;
    }
}






/** @brief Initializes peripherals for system boot.
*/
void init() {
    int ret;

    // Initialize the flash peripheral to enable access to persistent memory
    flash_simple_init();

    // Read starting flash values into our flash status struct
    flash_simple_read(FLASH_STATUS_ADDR, &decoder_status, sizeof(flash_entry_t));
    if (decoder_status.first_boot != FLASH_FIRST_BOOT) {
        /* If this is the first boot of this decoder, mark all channels as unsubscribed.
        *  This data will be persistent across reboots of the decoder. Whenever the decoder
        *  processes a subscription update, this data will be updated.
        */
        print_debug("First boot.  Setting flash...\n");

        decoder_status.first_boot = FLASH_FIRST_BOOT;

        channel_status_t subscription[MAX_CHANNEL_COUNT];

        for (int i = 0; i < MAX_CHANNEL_COUNT; i++){
            subscription[i].start_timestamp = DEFAULT_CHANNEL_TIMESTAMP;
            subscription[i].end_timestamp = DEFAULT_CHANNEL_TIMESTAMP;
            subscription[i].active = false;
        }

        // Write the starting channel subscriptions into flash.
        memcpy(decoder_status.subscribed_channels, subscription, MAX_CHANNEL_COUNT*sizeof(channel_status_t));

        flash_simple_erase_page(FLASH_STATUS_ADDR);
        flash_simple_write(FLASH_STATUS_ADDR, &decoder_status, sizeof(flash_entry_t));
    }

    // Initialize the uart peripheral to enable serial I/O
    ret = uart_init();
    if (ret < 0) {
        STATUS_LED_ERROR();
        // if uart fails to initialize, do not continue to execute
        while (1);
    }
}

/* Code between this #ifdef and the subsequent #endif will
*  be ignored by the compiler if CRYPTO_EXAMPLE is not set in
*  the projectk.mk file. */
#ifdef CRYPTO_EXAMPLE
void crypto_example(void) {
    // Example of how to utilize included simple_crypto.h

    // This string is 16 bytes long including null terminator
    // This is the block size of included symmetric encryption
    char *data = "Crypto Example!";
    uint8_t ciphertext[BLOCK_SIZE];
    uint8_t key[KEY_SIZE];
    uint8_t hash_out[HASH_SIZE];
    uint8_t decrypted[BLOCK_SIZE];

    char output_buf[128] = {0};

    // Zero out the key
    bzero(key, BLOCK_SIZE);

    // Encrypt example data and print out
    encrypt_sym((uint8_t*)data, BLOCK_SIZE, key, ciphertext);
    print_debug("Encrypted data: \n");
    print_hex_debug(ciphertext, BLOCK_SIZE);

    // Hash example encryption results
    hash(ciphertext, BLOCK_SIZE, hash_out);

    // Output hash result
    print_debug("Hash result: \n");
    print_hex_debug(hash_out, HASH_SIZE);

    // Decrypt the encrypted message and print out
    decrypt_sym(ciphertext, BLOCK_SIZE, key, decrypted);
    sprintf(output_buf, "Decrypted message: %s\n", decrypted);
    print_debug(output_buf);
}
#endif  //CRYPTO_EXAMPLE

/**********************************************************
 *********************** MAIN LOOP ************************
 **********************************************************/

 #include <stdio.h>
 #include <stdint.h>
 
 int main(void) {
     char output_buf[128] = {0}; // Buffer for formatted debug messages
     uint8_t uart_buf[100];
     msg_type_t cmd;
     int result;
     uint16_t pkt_len;
 
     // Initialize the device
     init();
 
     // Debug: Boot message
     print_debug("Decoder Booted!");
 
     // Print size of frame_packet_t
     sprintf(output_buf, "Size of frame_packet_t: %d bytes", (int)sizeof(frame_packet_t));
     print_debug(output_buf);
 
     // Print size of pkt_len
     sprintf(output_buf, "Size of pkt_len: %d bytes", (int)sizeof(pkt_len));
     print_debug(output_buf);
 
     // Process commands forever
     while (1) {
         print_debug("Ready");
 
         //STATUS_LED_GREEN();
         STATUS_LED_WHITE();
 
         result = read_packet(&cmd, uart_buf, &pkt_len);
 
         // Debug: Print command received
         sprintf(output_buf, "Received Command: %d", cmd);
         print_debug(output_buf);
 
         // Debug: Print packet length
         sprintf(output_buf, "Packet Length: %d bytes", pkt_len);
         print_debug(output_buf);
 
         if (result < 0) {
             STATUS_LED_ERROR();
             print_error("Failed to receive cmd from host");
             continue;
         }
 
         // Handle the requested command
         switch (cmd) {
         case LIST_MSG:
             STATUS_LED_CYAN();
             print_debug("Executing: LIST_MSG");
             list_channels();
             break;
 
         case DECODE_MSG:
             STATUS_LED_PURPLE();
             print_debug("Executing: DECODE_MSG");
             decode(pkt_len, uart_buf);
             break;
 
         case SUBSCRIBE_MSG:
             STATUS_LED_YELLOW();
             print_debug("Executing: SUBSCRIBE_MSG");
             update_subscription(pkt_len, (subscription_update_packet_t *)uart_buf);
             break;
 
         default:
             STATUS_LED_ERROR();
             sprintf(output_buf, "Invalid Command: %c", cmd);
             print_error(output_buf);
             break;
         }
     }
 }
 