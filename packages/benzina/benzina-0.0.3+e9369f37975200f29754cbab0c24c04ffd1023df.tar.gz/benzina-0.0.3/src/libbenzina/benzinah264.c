/* Includes */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "benzina/benzina.h"


/* Defines */



/* Data Structure Definitions */
typedef struct BENZINA_H264_SPS                      BENZINA_H264_SPS;
typedef struct BENZINA_H264_PPS                      BENZINA_H264_PPS;
typedef struct BENZINA_H264_SEI_DISPLAY_ORIENTATION  BENZINA_H264_SEI_DISPLAY_ORIENTATION;
typedef struct BENZINA_H264_READER                   BENZINA_H264_READER;

struct BENZINA_H264_READER{
	ssize_t  rd(void* rdr, void* buf, size_t len);
	void*    rdr;
	struct{
		uint64_t zeroBytes : 3;
		uint64_t inNALU    : 1;
		uint64_t inSEI     : 1;
	} status;
	uint8_t  buf[32];
};

/**
 * @brief Sequence Parameter Set
 * 
 * Reference: ITU-T H.264 7.3.2.1.1 & 7.4.2.1.1
 */

struct BENZINA_H264_SPS{
	uint64_t present                                :  1;
	uint64_t profile_idc                            :  8;
	uint64_t constraint_set0_flag                   :  1;
	uint64_t constraint_set1_flag                   :  1;
	uint64_t constraint_set2_flag                   :  1;
	uint64_t constraint_set3_flag                   :  1;
	uint64_t constraint_set4_flag                   :  1;
	uint64_t constraint_set5_flag                   :  1;
	uint64_t reserved_zero_2bits                    :  2;/* Range: 0 */
	uint64_t level_idc                              :  8;
	uint64_t seq_parameter_set_id                   :  5;/* Range: 0-31 */
	
	uint64_t chroma_format_idc                      :  3;/* Range: 0-3, potential future extension */
	uint64_t separate_colour_plane_flag             :  1;
	uint64_t bit_depth_luma_minus8                  :  7;/* Range: 0-6, potential future extension */
	uint64_t bit_depth_chroma_minus8                :  7;/* Range: 0-6, potential future extension */
	uint64_t qpprime_y_zero_transform_bypass_flag   :  1;
	
	uint8_t  seq_scaling_list_4x4[6][4*4];
	uint8_t  seq_scaling_list_8x8[6][8*8];
	
	uint64_t log2_max_frame_num_minus4              :  4;/* Range: 0-12 */
	uint64_t pic_order_cnt_type                     :  2;/* Range: 0-2 */
	uint64_t log2_max_pic_order_cnt_lsb_minus4      :  4;/* Range: 0-12 */
	uint64_t delta_pic_order_always_zero_flag       :  1;
	int32_t  offset_for_non_ref_pic;
	int32_t  offset_for_top_to_bottom_field;
	uint8_t  num_ref_frames_in_pic_order_cnt_cycle;      /* Range: 0-255 */
	int32_t  offset_for_ref_frame[255];
	uint64_t max_num_ref_frames                     :  5;/* Range: 0-16 */
	uint64_t gaps_in_frame_num_value_allowed_flag   :  1;
	uint32_t pic_width_in_mbs_minus1;
	uint32_t pic_height_in_map_units_minus1;
	uint64_t frame_mbs_only_flag                    :  1;
	uint64_t mb_adaptive_frame_field_flag           :  1;
	uint64_t direct_8x8_inference_flag              :  1;
	uint64_t frame_cropping_flag                    :  1;
	uint32_t frame_crop_left_offset;
	uint32_t frame_crop_right_offset;
	uint32_t frame_crop_top_offset;
	uint32_t frame_crop_bottom_offset;
	struct{
		uint64_t present                                :  1;
		uint64_t aspect_ratio_info_present_flag         :  1;
		uint64_t aspect_ratio_idc                       :  8;
		uint64_t sar_width                              : 16;
		uint64_t sar_height                             : 16;
		uint64_t overscan_info_present_flag             :  1;
		uint64_t overscan_appropriate_flag              :  1;
		uint64_t video_signal_type_present_flag         :  1;
		uint64_t video_format                           :  3;
		uint64_t video_full_range_flag                  :  1;
		uint64_t colour_description_present_flag        :  1;
		uint64_t colour_primaries                       :  8;
		uint64_t transfer_characteristics               :  8;
		uint64_t matrix_coefficients                    :  8;
		uint64_t chroma_loc_info_present_flag           :  1;
		uint64_t chroma_sample_loc_type_top_field       :  3;
		uint64_t chroma_sample_loc_type_bottom_field    :  3;
		uint64_t timing_info_present_flag               :  1;
		uint64_t num_units_in_tick                      : 32;
		uint64_t time_scale                             : 32;
		uint64_t fixed_frame_rate_flag                  :  1;
		struct{
			struct{
				uint64_t present                                :  1;
				uint64_t cpb_cnt_minus1                         :  5;/* Range: 0-31 */
				uint64_t bit_rate_scale                         :  4;
				uint64_t cpb_size_scale                         :  4;
				uint32_t bit_rate_value_minus1[32];
				uint32_t cpb_size_value_minus1[32];
				uint64_t cbr_flags                              : 32;
				uint64_t initial_cpb_removal_delay_length_minus1:  5;
				uint64_t cpb_removal_delay_length_minus1        :  5;
				uint64_t dpb_output_delay_length_minus1         :  5;
				uint64_t time_offset_length                     :  5;
			} nal, vcl;
		} hrd;
		uint64_t low_delay_hrd_flag                     :  1;
		uint64_t pic_struct_present_flag                :  1;
		uint64_t bitstream_restriction_flag             :  1;
		uint64_t motion_vectors_over_pic_boundaries_flag:  1;
		uint64_t max_bytes_per_pic_denom                :  5;/* Range: 0-16 */
		uint64_t max_bits_per_mb_denom                  :  5;/* Range: 0-16 */
		uint64_t log2_max_mv_length_horizontal          :  5;/* Range: 0-16 */
		uint64_t log2_max_mv_length_vertical            :  5;/* Range: 0-16 */
		uint64_t max_num_reorder_frames                 :  5;/* Range: 0-16 */
		uint64_t max_dec_frame_buffering                :  5;/* Range: 0-16 */
	} vui;
};

/**
 * @brief Picture Parameter Set
 * 
 * Reference: ITU-T H.264 7.3.2.2 & 7.4.2.2
 */

struct BENZINA_H264_PPS{
	uint64_t present                                      :  1;
	uint64_t pic_parameter_set_id                         :  8;/* Range: 0-255 */
	uint64_t seq_parameter_set_id                         :  5;/* Range: 0-31 */
	uint64_t entropy_coding_mode_flag                     :  1;
	uint64_t bottom_field_pic_order_in_frame_present_flag :  1;
	uint64_t num_slice_groups_minus1                      :  3;/* Range: 0-7 */
	/* Only value of num_slice_groups_minus1 supported is 0. */
	uint64_t num_ref_idx_l0_default_active_minus1         :  5;/* Range: 0-31 */
	uint64_t num_ref_idx_l1_default_active_minus1         :  5;/* Range: 0-31 */
	uint64_t weighted_pred_flag                           :  1;
	uint64_t weighted_bipred_idc                          :  2;
	int64_t  pic_init_qp_minus26                          :  6;/* Range: -26-+25 */
	int64_t  pic_init_qs_minus26                          :  6;/* Range: -26-+25 */
	int64_t  chroma_qp_index_offset                       :  5;/* Range: -12-+12 */
	uint64_t deblocking_filter_control_present_flag       :  1;
	uint64_t constrained_intra_pred_flag                  :  1;
	uint64_t redundant_pic_cnt_present_flag               :  1;
	
	uint64_t transform_8x8_mode_flag                      :  1;
	int64_t  second_chroma_qp_index_offset                :  5;/* Range: -12-+12 */
	
	uint8_t  seq_scaling_list_4x4[6][4*4];
	uint8_t  seq_scaling_list_8x8[6][8*8];
};

/**
 * @brief Display Orientation SEI
 * 
 * Reference: ITU-T H.264 D.1.26 & D.2.26
 */

struct BENZINA_H264_SEI_DISPLAY_ORIENTATION{
	uint64_t present                                      :  1;
	uint64_t cancel                                       :  1;
	uint64_t hor_flip                                     :  1;
	uint64_t ver_flip                                     :  1;
	uint64_t ccw_rotation                                 : 16;/* Range: 0-65535; Units are 1/2^16ths of full circle */
	uint64_t display_orientation_repetition_period        : 16;/* Range: 0-16384 */
	uint64_t display_orientation_extension_flag           :  1;
};



/* Static Function Declarations */

