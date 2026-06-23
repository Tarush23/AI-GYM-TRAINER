import streamlit as st

from services.config.workout_config import (
    EXERCISE_OPTIONS
)
import time

from services.coaching.voice_pipeline import autoplay_audio


def render_sidebar():
    username = st.session_state.get("username")    
    with st.sidebar:
        st.title("Apna AI Coach")

        st.caption(f"login as {username}")
        st.divider()

        st.subheader("Workout Plan")

        if st.session_state.get("audio_to_play"):
            autoplay_audio(st.session_state.audio_to_play)

        if st.session_state.get("coach_feedback"):
            st.markdown("")
            st.success(f"**Coach:**{st.session_state.coach_feedback}")

        if not st.session_state.get("workout_started"):

            plan_exercise = st.selectbox(
                "Exercise",
                options=EXERCISE_OPTIONS,
                key="plan_exercise"
            )

            plan_sets = st.number_input(
                "Sets",
                min_value=0,
                max_value=50,
                step=1,
                key="plan_sets"
            )

            plan_reps = st.number_input(
                "Reps per Set",
                min_value=0,
                max_value=50,
                step=1,
                key="plan_reps"
            )

            st.markdown("")

            start_session_button = st.button(
                "Start Workout",
                width="stretch",
                key="start_session_button"
            )

            if start_session_button:
                # Save actual workout config
                st.session_state.exercise = plan_exercise
                st.session_state.target_sets = int(plan_sets)
                st.session_state.reps_per_set = int(plan_reps)

                # Reset progress
                st.session_state.reps = 0
                st.session_state.current_set_reps = 0
                st.session_state.sets_completed = 0

                # Start session
                st.session_state.workout_started = True

                # Tracking values
                st.session_state.set_cycle_started_at = time.time()
                st.session_state.last_saved_sets_completed = 0
                st.session_state.last_notified_sets_completed = 0
                st.session_state.last_notified_workout_complete = False

                if st.session_state.get("voice_pipeline"):
                    result = st.session_state.voice_pipeline.process_event(
                        event = "workout_started",
                        exercise = plan_exercise,
                        metrics={}
                    )

                    if result:
                        st.session_state.audio_to_play,st.session_state.coach_feedback = result


                st.rerun()
            
        if st.session_state.get("workout_started"):
            st.write("workout started")

            exercise = st.session_state.exercise
            sets = st.session_state.target_sets
            reps = st.session_state.reps_per_set

            st.info(f"**{exercise}** --{sets}Sets/{reps}Reps")
            
            end_session_button = st.button("end workout",key="end_session_button")

            if end_session_button:
                if st.session_state.get("voice_pipeline"):
                    result = st.session_state.voice_pipeline.process_event(
                        event="workout_completed",
                        exercise = exercise,
                        metrics = {}
                    )

                    if result:
                        st.session_state.audio_to_play,st.session_state.coach_feedback = result
                        #time.sleep(2)


                st.session_state["workout_started"] = False
                st.session_state["exercise"] = None
                st.session_state["target_sets"] = 0
                st.session_state["reps_per_set"] = 0
                st.session_state["reps"] = 0
                st.session_state["current_set_reps"] = 0
                st.session_state["sets_completed"] = 0
                st.session_state["coach_feedback"] = None
                st.session_state["audio_to_play"] = None
                st.rerun()


            st.divider()

            st.subheader("Progress")

            exercise = st.session_state.get("exercise")
            total_reps = st.session_state.get("reps")
            current_set_reps = st.session_state.get("current_set_reps")

            reps_per_set = st.session_state.get("reps_per_set")

            sets_completed = st.session_state.get("sets_completed")

            target_sets = st.session_state.get("target_sets")

            st.metric("Total reps",f"{total_reps}")
            st.metric("current set reps",f"{current_set_reps}/{reps_per_set}")
            st.metric("sets completed",f"{sets_completed}/{target_sets}")


            st.divider()
            st.subheader(f"{exercise} Metrics")

            match exercise:
                case "Squats":
                    st.metric("Knee Angle", f"{st.session_state.knee_angle}°")
                    st.metric("Back Angle", f"{st.session_state.back_angle}°")
                    st.metric("Depth Status", st.session_state.depth_status)

                case "Push-ups":
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                    st.metric("Body Alignment", st.session_state.body_alignment)
                    st.metric("Hip Position", st.session_state.hip_status)

                case "Biceps Curls(Dumbell)":
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                    st.metric("Shoulder Stability", st.session_state.shoulder_status)
                    st.metric("Swing Detection", st.session_state.swing_status)

                case "Shoulder Press":
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                    st.metric("Arm Extension", st.session_state.extension_status)
                    st.metric("Back Arch", st.session_state.back_arch_status)

                case "Lunges":
                    st.metric("Front Knee Angle", f"{st.session_state.front_knee_angle}°")
                    st.metric("Torso Angle", f"{st.session_state.torso_angle}°")
                    st.metric("Balance Status", st.session_state.balance_status)




